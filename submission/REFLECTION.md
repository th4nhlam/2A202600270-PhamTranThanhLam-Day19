# Reflection — Lab 19

**Tên:** Pham Tran Thanh Lam
**Cohort:** A20-K1
**Path đã chạy:** lite

---

## Câu hỏi (≤ 200 chữ)

> Trên golden set 50 queries, mode nào thắng ở loại query nào (`exact` /
> `paraphrase` / `mixed`), và tại sao? Khi nào bạn **không** dùng hybrid
> (i.e. khi nào pure BM25 hoặc pure vector là lựa chọn đúng)?

- Exact queries: BM25/hybrid thắng (hoặc ngang nhau) vì query chứa các từ khóa kỹ thuật khớp chính xác văn bản trong tập tài liệu, đây là lợi thế mạnh nhất của lexical search.
- Paraphrase queries: Vector/hybrid thắng một cách tương đối nhưng tổng quan thì điểm thấp hơn. Do semantic search có thể ánh xạ những từ đồng nghĩa nhưng model `BAAI/bge-small-en-v1.5` trên dataset tiếng Việt vẫn chưa đủ tối ưu cho task này.
- Mixed queries: Hybrid thắng tuyệt đối (100%). Sự kết hợp RRF (Reciprocal Rank Fusion) giúp bắt được các keywords quan trọng từ BM25, cùng lúc hiểu ngữ cảnh khái quát từ vector, là lựa chọn mạnh mẽ nhất trong thực tế.

Không nên dùng hybrid khi chỉ tìm kiếm ID tài liệu, email, mã code chính xác (BM25 tốt nhất) hoặc khi hệ thống gặp rào cản lớn về tốc độ latency/tài nguyên (Vector hoặc BM25 tốn ít chi phí hơn).

---

## Điều ngạc nhiên nhất khi làm lab này

Vector embedding đôi khi bắt trượt ý nghĩa trong tiếng Việt nếu dùng một model nhỏ tiếng Anh, dẫn đến recall của paraphrase queries bị tụt đáng kể.

---

## Bonus challenge

- [x] Đã làm bonus (xem `bonus/`)
- [ ] Pair work với: 
