# Notebooks — Pipeline phát hiện xâm nhập NSL-KDD

Sáu notebook tương ứng sáu đầu việc kỹ thuật của đề tài (mục 6 trong
[`docs/01-phan-tich-de-tai.md`](../docs/01-phan-tich-de-tai.md)).

## Thứ tự chạy

| # | Notebook | Đầu việc | Sản phẩm chính |
|---|---|---|---|
| 01 | [01-tien-xu-ly.ipynb](./01-tien-xu-ly.ipynb) | Tiền xử lý, encode, chuẩn hóa | `data/processed/X_*.npy`, `y_*.npy` |
| 02 | [02-clustering.ipynb](./02-clustering.ipynb) | K-Means & DBSCAN trên Normal | nhãn cụm, nhãn noise |
| 03 | [03-do-do-khoang-cach.ipynb](./03-do-do-khoang-cach.ipynb) | Euclidean & Mahalanobis | anomaly scores |
| 04 | [04-phat-hien-di-biet.ipynb](./04-phat-hien-di-biet.ipynb) | Ngưỡng + metric | nhãn Normal/Attack, bảng metric |
| 05 | [05-so-sanh-mo-hinh.ipynb](./05-so-sanh-mo-hinh.ipynb) | Unsupervised vs supervised | bảng metric tổng hợp |
| 06 | [06-tan-cong-moi.ipynb](./06-tan-cong-moi.ipynb) | Đánh giá 17 loại tấn công mới | recall theo loại/họ |

## Quy ước

- Chạy Jupyter từ **thư mục gốc dự án**: `jupyter lab`.
- Mỗi notebook tự thêm thư mục gốc vào `sys.path` và import package `nids/`
  (`nids.config` cho hằng số, `nids.data` cho hàm nạp dữ liệu).
- Artifact trung gian lưu ở `data/processed/` (đã gitignore).
- Hình vẽ lưu ở `reports/figures/`.
- Cố định `RANDOM_STATE = 42` để tái lập kết quả.
