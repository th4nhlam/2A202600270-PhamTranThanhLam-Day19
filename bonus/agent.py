import sys
from pathlib import Path
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from feast import FeatureStore

class HybridMemoryAgent:
    def __init__(self):
        self.embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        self.qdrant = QdrantClient(":memory:")
        self.qdrant.create_collection(
            collection_name="episodic_memory",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        self.next_memory_id = 0
        
        self.feast_dir = ROOT / "app" / "feast_repo"
        self.fs = FeatureStore(repo_path=str(self.feast_dir))
        
        self.profile_features = [
            "user_profile_features:reading_speed_wpm",
            "user_profile_features:preferred_language",
            "user_profile_features:topic_affinity",
            "query_velocity_features:queries_last_hour",
            "query_velocity_features:distinct_topics_24h",
        ]

    def remember(self, text: str, user_id: str = "u_001") -> None:
        """Add a new piece of episodic memory for this user."""
        vector = list(self.embedder.embed([text]))[0].tolist()
        self.qdrant.upsert(
            collection_name="episodic_memory",
            points=[
                PointStruct(
                    id=self.next_memory_id,
                    vector=vector,
                    payload={"user_id": user_id, "text": text, "timestamp": datetime.now(timezone.utc).isoformat()}
                )
            ]
        )
        self.next_memory_id += 1

    def recall(self, query: str, user_id: str = "u_001") -> str:
        """Retrieve top-K memories + user profile features → return assembled context."""
        features = self.fs.get_online_features(
            features=self.profile_features,
            entity_rows=[{"user_id": user_id}],
        ).to_dict()
        
        speed = features.get("reading_speed_wpm", ["Unknown"])[0]
        topic = features.get("topic_affinity", ["Unknown"])[0]
        queries_last_hour = features.get("queries_last_hour", [0])[0]

        q_vec = list(self.embedder.embed([query]))[0].tolist()
        
        res = self.qdrant.query_points(
            collection_name="episodic_memory", 
            query=q_vec, 
            limit=3,
            query_filter=Filter(
                must=[
                    FieldCondition(key="user_id", match=MatchValue(value=user_id))
                ]
            )
        )
        
        memories = [p.payload["text"] for p in res.points]
        
        memory_str = "\n".join(f"- {m}" for m in memories) if memories else "No relevant memories found."
        
        context = (
            f"User likes <{topic}> reading at <{speed}>wpm.\n"
            f"Recent activity: <{queries_last_hour}> queries in the last hour.\n"
            f"Top memories:\n{memory_str}"
        )
        
        return context
