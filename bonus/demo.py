import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from bonus.agent import HybridMemoryAgent

def main():
    print("Initializing agent...")
    agent = HybridMemoryAgent()
    
    print("Adding memories...")
    agent.remember("Tôi đã đọc một bài rất hay về Kubernetes và container orchestration.")
    agent.remember("Gần đây tôi đang tìm hiểu về cloud security và IAM roles.")
    agent.remember("Hệ thống tự động mở rộng (auto-scaling) rất quan trọng trong hệ thống phân tán.")
    
    queries = [
        "Tôi đã đọc gì về Kubernetes?",
        "Recommend đọc gì tiếp",
        "Tôi đang quan tâm gì gần đây?",
        "Tài liệu về tự động mở rộng hạ tầng?",
        "Cho tôi summary cloud security"
    ]
    
    print("="*50)
    for i, q in enumerate(queries, 1):
        print(f"\nQuery {i}: {q}")
        print("-" * 50)
        context = agent.recall(q, user_id="u_001")
        print(context)
        print("=" * 50)

if __name__ == "__main__":
    main()
