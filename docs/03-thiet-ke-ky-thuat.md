# 03 — Thiết kế kỹ thuật

> Tài liệu này chốt **cách làm** của dự án: pipeline tiền xử lý, chọn tham số clustering,
> cách tính điểm dị biệt, cách chọn ngưỡng, và thiết kế so sánh unsupervised vs supervised.
> Các con số lấy từ notebook 01–06 (`RANDOM_STATE = 36` theo `nids/config.py`).

---

## 1. Quy ước chung

- **Nhiệm vụ chính**: bài toán **nhị phân** (Normal vs Attack). Bài toán đa lớp theo 5 họ
  (Normal/DoS/Probe/R2L/U2R) chỉ dùng để *phân tích* (recall theo họ), không dùng để train
  multiclass trong pipeline này.
- **Unsupervised chỉ học từ Normal**: K-Means, DBSCAN, Mahalanobis đều fit trên
  `train[Normal]` (67.343 mẫu). Không dùng nhãn attack để học phân phối "bình thường".
- **Ngưỡng chỉ chọn trên train**: tránh rò rỉ (leakage) từ test.
- **Baseline supervised** học từ toàn bộ train có nhãn (125.973 mẫu, 46.5% attack).
- **Hạt giống ngẫu nhiên**: `RANDOM_STATE = 36` dùng chung cho `numpy` và mọi estimator
  có `random_state`.

## 2. Tiền xử lý (notebook 01)

| Bước | Cách làm | Chi tiết |
|---|---|---|
| Bỏ cột | Drop `difficulty` và đặc trưng hằng `num_outbound_cmds` | Hằng số làm ma trận hiệp phương sai suy biến |
| Encode | `OneHotEncoder(handle_unknown="ignore")` trên `protocol_type`, `service`, `flag` | Fit **chỉ trên train**; sinh 84 cột (3 + 70 + 11) |
| Chuẩn hóa | `StandardScaler` trên 37 biến số | Fit **chỉ trên train**, transform cả train/test |
| Ma trận cuối | Ghép `[37 biến số \| 84 cột one-hot]` = **121 chiều** | `X_train (125973, 121)`, `X_test (22544, 121)` |

Artifact lưu ở `data/processed/`: `X_train.npy`, `X_test.npy`, `y_*_binary.npy`,
`y_*_family.npy`, `features.json`.

## 3. Clustering (notebook 02)

- **K-Means**: fit trên train-Normal, `k` chọn bằng **elbow + silhouette** trên mẫu
  5.000 Normal (silhouette toàn bộ 67k quá chậm). Inertia giảm nhanh tới k=6–7 rồi chậm
  dần sau k=8; silhouette tốt ở các k lớn. Chốt **`k = 8`**, `n_init=10`.
  Lưu `kmeans_centers.npy` (8×121) và nhãn cụm cho train.
- **DBSCAN (tham chiếu)**: DBSCAN trong 121 chiều rất chậm và nhạy với `eps`, nên giảm
  xuống **PCA-10** (giữ 78.1% phương sai) và fit trên mẫu 10.000 Normal. Với
  `eps=5.0`, `min_samples=100` được **2 cụm** và noise **0.93%** trên Normal.
  Lưu cấu hình vào `config.json`.
- Trực quan hóa: PCA 2D lưu `02_clusters_pca.png`.

## 4. Điểm dị biệt (notebook 03)

- **Euclidean**: `d(x) = min_k ||x − c_k||` với các tâm K-Means. Đơn giản, nhạy với thang đo
  (đã chuẩn hóa) và với chiều ít thông tin.
- **Mahalanobis**: `d(x) = sqrt((x−μ)ᵀ Σ⁻¹ (x−μ))` với `μ`, `Σ` ước lượng trên train-Normal.
  Dùng **`pinv(Σ)`** (pseudo-inverse) thay vì nghịch đảo thường vì `Σ` 121×121 dễ suy biến.
  Tính bằng dạng toàn phương `einsum` để nhanh mà không tạo ma trận trung gian lớn.
- Lưu 4 file điểm: `score_euclidean_{train,test}.npy`, `score_mahalanobis_{train,test}.npy`.
- Trực quan hóa: `03_score_distribution.png`.

## 5. Ngưỡng (notebook 04)

- **Percentile trên Normal (p95)**: ngưỡng sao cho 5% Normal bị báo nhầm trên *train*.
  Đây là cách chốt cho pipeline.
- **Chi-square**: ngưỡng `sqrt(chi2.ppf(0.95, df=d))` với `d` = số chiều đặc trưng (121),
  chỉ áp dụng cho Mahalanobis bình phương. Dùng để **đối chiếu** độ chặt của ngưỡng.
- Output `y_pred_euclidean.npy`, `y_pred_mahalanobis.npy` (ngưỡng p95) được các notebook
  05–06 tái sử dụng.

## 6. So sánh unsupervised vs supervised (notebook 05)

| Nhóm | Mô hình | Học từ | Điểm số cho PR-AUC |
|---|---|---|---|
| Supervised | LogisticRegression (`max_iter=1000`) | toàn bộ train có nhãn | `predict_proba` |
| Supervised | RandomForest (`n_estimators=200`) | toàn bộ train có nhãn | `predict_proba` |
| Supervised | XGBoost (`n_estimators=300, max_depth=6`) | toàn bộ train có nhãn | `predict_proba` |
| Unsupervised | Euclidean tới tâm K-Means | train-Normal + ngưỡng p95 | anomaly score |
| Unsupervised | Mahalanobis trên Normal | train-Normal + ngưỡng p95 | anomaly score |

Cùng test set (22.544 mẫu), cùng metric (precision/recall/F1/PR-AUC) và thêm bảng
**recall theo họ** để thấy họ hiếm (R2L/U2R).

## 7. Novel attack (notebook 06)

- Novel = 17 tên chỉ xuất hiện ở test (`apache2, httptunnel, ...` — xem notebook 06).
  `novel_attack_types` trong `nids/data.py` tự suy ra từ train vs test.
- Tách test thành **known attack** (đã thấy ở train) và **novel** (3.750 dòng, 29.2% attack).
- Báo cáo recall tổng + recall theo họ + recall theo từng tên trong nhóm novel,
  và vẽ `06_novel_recall.png`.

## 8. Hạn chế đã biết

- DBSCAN chỉ là tham chiếu trên PCA-10 + mẫu 10.000, **không dùng làm scorer chính**.
- One-hot `service` tạo nhiều cột thưa; khoảng cách Euclid/Mahalanobis có thể bị nhiễu bởi
  chiều thưa này. Đây là hướng cải tiến (target/ frequency encoding, giảm chiều PCA trước
  khi chấm điểm).
- Ngưỡng p95 cố định một điểm vận hành; PR curve ở notebook 04 cho thấy toàn bộ đường
  đánh đổi để chọn ngưỡng khác khi triển khai.
