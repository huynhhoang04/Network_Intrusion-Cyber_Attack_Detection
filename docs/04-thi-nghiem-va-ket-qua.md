# 04 — Thí nghiệm & kết quả

> Mọi con số trong tài liệu này đều lấy từ output thực tế của 6 notebook.
> `RANDOM_STATE = 36`. Unsupervised fit trên train-Normal, ngưỡng p95 trên train-Normal;
> supervised fit trên toàn bộ train có nhãn; đánh giá trên test (22.544 mẫu).

---

## 1. Bảng kết quả tổng hợp (test)

### 1.1 Metric nhị phân

| Mô hình | Precision | Recall | F1 | PR-AUC |
|---|---|---|---|---|
| LogisticRegression (supervised) | 0.9176 | 0.6232 | 0.7423 | 0.8646 |
| RandomForest (supervised) | 0.9678 | 0.6160 | 0.7528 | 0.9636 |
| XGBoost (supervised) | 0.9681 | 0.6428 | 0.7726 | 0.9721 |
| Euclidean (unsupervised) | 0.8836 | 0.4352 | 0.5832 | 0.8839 |
| Mahalanobis (unsupervised) | 0.9370 | 0.8334 | 0.8822 | 0.9616 |

*(Notebook 05, ngưỡng p95 cho unsupervised; supervised dùng ngưỡng quyết định mặc định 0.5.)*

### 1.2 Điểm dị biệt và ngưỡng (notebook 03–04)

- Trung vị điểm trên test (Normal/Attack): Euclidean **1.44 / 4.98** (3.46×),
  Mahalanobis **1.97 / 23.28** (11.83×) → Mahalanobis tách tốt hơn rõ rệt.
- Ngưỡng p95 trên train-Normal: Euclidean **5.116**, Mahalanobis **14.733**;
  ngưỡng chi² (95%, d=121) cho Mahalanobis là **12.152** (chặt hơn, cho F1 0.8984
  nhỉnh hơn p95 là 0.8822).

### 1.3 Clustering (notebook 02)

- K-Means `k=8` trên train-Normal; elbow/silhouette trên mẫu 5.000 đã ghi ở notebook 02.
- DBSCAN trên PCA-10 + mẫu 10.000 Normal (`eps=5.0`, `min_samples=100`): 2 cụm,
  noise **0.93%** trên Normal. Vì DBSCAN nhạy tham số trong 121 chiều, nó chỉ đóng vai
  trò tham chiếu — scorer chính là Euclidean/Mahalanobis.

## 2. Recall theo họ tấn công (test, notebook 05)

| Mô hình | DoS | Probe | R2L | U2R | Normal (FPR) |
|---|---|---|---|---|---|
| LogisticRegression | 0.8193 | 0.7580 | 0.0125 | 0.2239 | 0.0739 |
| RandomForest | 0.7857 | 0.7720 | 0.0572 | 0.1493 | 0.0271 |
| XGBoost | 0.8509 | 0.7063 | 0.0620 | 0.1791 | 0.0280 |
| Euclidean (unsupervised) | 0.3184 | 0.8658 | 0.3723 | 0.5970 | 0.0758 |
| Mahalanobis (unsupervised) | 0.9083 | 0.9075 | 0.5795 | 0.7463 | 0.0740 |

Nhận xét: supervised **sụp đổ trên R2L** (0.01–0.06) vì họ quá hiếm ở train (995/125.973);
unsupervised không phụ thuộc danh sách tấn công nên bắt được 0.37–0.58 trên R2L và
0.60–0.75 trên U2R. Mahalanobis thắng Euclidean ở mọi họ nhờ tính phương sai/tương quan.

## 3. Tấn công mới (notebook 06)

Test có **3.750 dòng novel** (17 loại, 29.2% attack). Recall known vs novel:

| Mô hình | Known attack | Novel tổng | DoS novel | Probe novel | R2L novel | U2R novel |
|---|---|---|---|---|---|---|
| LogisticRegression | 0.7131 | 0.4056 | 0.4252 | 0.5924 | 0.0102 | 0.1333 |
| RandomForest | 0.7702 | 0.2424 | 0.0780 | 0.5802 | 0.0087 | 0.2000 |
| XGBoost | 0.7727 | 0.3283 | 0.3566 | 0.4593 | 0.0102 | 0.2333 |
| Euclidean (unsupervised) | 0.4741 | 0.3411 | 0.0977 | 0.7985 | 0.0656 | 0.5333 |
| Mahalanobis (unsupervised) | 0.8752 | 0.7323 | 0.8016 | 0.8973 | 0.2420 | 0.7333 |

**Nếu không chia known/novel**, khoảng cách giữa các mô hình bị che khuất
(ví dụ RF vẫn giữ known recall 0.77 nhưng novel chỉ 0.24).

### 3.1 Theo từng tên novel (rút gọn)

- Bắt tốt bởi Mahalanobis: `apache2` 0.9973, `httptunnel` 0.9925, `mscan` 0.9789,
  `sqlattack` 1.00, `xsnoop` 1.00, `processtable` 0.9314, `xlock` 0.8889.
- Chỉsupervised bắt được: `udpstorm` (RF/XGB 1.00, Mahalanobis 0.00),
  `saint` (mọi mô hình đều cao, 0.64–0.99).
- Gần như **bị bỏ sót bởi tất cả**: `worm` (0.00 mọi mô hình), `snmpguess` (0.00),
  `snmpgetattack` (≤0.05), `mailbomb` (≤0.02). Đây là giới hạn của cả hai hướng.

## 4. Kết luận

1. **Mahalanobis là phương án tốt nhất cho mục tiêu đề tài** (tấn công mới):
   novel recall 0.73, cao gấp đôi LogReg và gấp ba RF, đặc biệt mạnh trên U2R/R2L.
2. **Supervised không thua trên known attack** (XGB F1 0.77, Mahalanobis 0.88) nhưng
   **không tổng quát hóa** với signature mới, nhất là họ hiếm.
3. **Giá của unsupervised là FPR cao** (~7.4% so với RF/XGB ~2.8%) — cần chọn ngưỡng theo
   yêu cầu vận hành (chi² cho kết quả nhỉnh hơn p95).
4. Hướng đi tiếp: giảm chiều PCA trước khi chấm điểm, thử `minPts`/encode khác cho
   `service`, và hiệu chuẩn ngưỡng theo PR curve.

Hình minh họa: `02_clusters_pca.png`, `03_score_distribution.png`, `04_pr_curve.png`,
`06_novel_recall.png` trong `reports/figures/`.

