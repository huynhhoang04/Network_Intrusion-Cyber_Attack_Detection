# Tài liệu dự án — Network Intrusion & Cyber Attack Detection

Thư mục này chứa tài liệu của dự án, viết bằng tiếng Việt, ưu tiên dễ hiểu.

## Danh sách tài liệu

| # | Tài liệu | Nội dung | Trạng thái |
|---|---|---|---|
| 01 | [Phân tích đề tài](./01-phan-tich-de-tai.md) | Đề tài là gì, phải làm gì, dữ liệu NSL-KDD ra sao | ✅ Hoàn thành |
| 02 | Thiết kế kỹ thuật | Pipeline tiền xử lý, clustering, distance, thí nghiệm | ⏳ Dự kiến |
| 03 | Thí nghiệm & kết quả | Cấu hình thí nghiệm, bảng kết quả, nhận xét | ⏳ Dự kiến |
| 04 | Báo cáo tổng hợp | Báo cáo cuối kỳ | ⏳ Dự kiến |

## Quy ước

- Số liệu trong tài liệu được sinh từ dữ liệu thật bằng `scripts/profile_data.py`.
- Thuật ngữ chuyên ngành được giải thích ngay lần đầu xuất hiện; xem thêm bảng thuật ngữ ở cuối tài liệu 01.
- Mỗi tài liệu tập trung vào một câu hỏi lớn để dễ đọc và dễ bảo trì.

## Cấu trúc dự án liên quan

```
data/raw/            # dữ liệu gốc NSL-KDD (KDDTrain+, KDDTest+)
scripts/
  download_data.py   # tải + verify dataset
  profile_data.py    # in thống kê mô tả dữ liệu
docs/                # tài liệu (thư mục này)
TOPIC.md             # mục tiêu đề tài
```
