# 02 — Giải thích thuật ngữ chuyên ngành

> Tài liệu tra cứu nhanh các thuật ngữ dùng trong dự án.
> Cách dùng: tìm theo nhóm bên dưới hoặc `Ctrl+F` theo từ khóa (cả tiếng Việt và tiếng Anh).
> Giải thích ưu tiên trực quan, kèm công thức/ví dụ khi cần.

---

## Mục lục

1. [An ninh mạng & phát hiện xâm nhập](#1-an-ninh-mạng--phát-hiện-xâm-nhập)
2. [Dữ liệu & tiền xử lý](#2-dữ-liệu--tiền-xử-lý)
3. [Học máy](#3-học-máy)
4. [Phân cụm (Clustering)](#4-phân-cụm-clustering)
5. [Độ đo khoảng cách (Distance)](#5-độ-đo-khoảng-cách-distance)
6. [Đánh giá mô hình (Evaluation)](#6-đánh-giá-mô-hình-evaluation)
7. [Thuật ngữ riêng của NSL-KDD](#7-thuật-ngữ-riêng-của-nsl-kdd)

---

## 1. An ninh mạng & phát hiện xâm nhập

| Thuật ngữ | English | Giải thích |
|---|---|---|
| **Xâm nhập** | Intrusion | Hành vi truy cập/hành động trái phép vào hệ thống mạng. |
| **IDS** | Intrusion Detection System | Hệ thống **phát hiện** xâm nhập: theo dõi traffic và báo động khi thấy bất thường. Chỉ báo, không chặn. |
| **IPS** | Intrusion Prevention System | Như IDS nhưng **chủ động chặn** kết nối nguy hiểm. |
| **Phát hiện dựa trên chữ ký** | Signature-based detection | So khớp traffic với "dấu vân tay" tấn công đã biết. Chính xác với cái đã biết, **mù** với cái mới. |
| **Phát hiện dựa trên dị biệt** | Anomaly-based detection | Học cái "bình thường" rồi báo cái lệch. Bắt được tấn công mới, nhưng dễ báo nhầm. |
| **Tấn công zero-day** | Zero-day attack | Tấn công khai thác lỗ hổng chưa được công bố/chưa có bản vá. |
| **Tấn công mới** | Novel attack | Loại tấn công **chưa từng xuất hiện trong tập huấn luyện**. |
| **Báo nhầm** | False positive (FP) | Hệ thống báo "tấn công" nhưng thực ra là bình thường. |
| **Bỏ sót** | False negative (FN) | Hệ thống báo "bình thường" nhưng thực ra là tấn công. |
| **DoS** | Denial of Service | Tấn công làm cạn kiệt tài nguyên khiến dịch vụ không phục vụ được. |
| **DDoS** | Distributed DoS | DoS từ nhiều máy cùng lúc (thường qua botnet). |
| **Probe / Quét cổng** | Probe / Port scan | Dò tìm cổng, dịch vụ, lỗ hổng đang mở để chuẩn bị tấn công. |
| **R2L** | Remote to Local | Kẻ tấn công từ xa tìm cách **chiếm quyền truy cập cục bộ** (ví dụ đoán mật khẩu). |
| **U2R** | User to Root | Từ quyền người dùng thường **leo thang lên quyền root** (quản trị cao nhất). |
| **Botnet** | Botnet | Mạng lưới máy bị nhiễm mã độc, bị điều khiển từ xa. |
| **Mã độc** | Malware | Phần mềm độc hại (virus, worm, trojan…). |
| **Rootkit** | Rootkit | Bộ công cụ ẩn mình trong hệ thống để duy trì quyền truy cập trái phép. |
| **Shell / Root shell** | Shell / Root shell | Giao diện dòng lệnh điều khiển máy; "root shell" là shell có toàn quyền. |
| **Khai thác lỗ hổng** | Exploit | Đoạn mã/hành động lợi dụng lỗ hổng để tấn công. |
| **Phần tải** | Payload | Phần "hàng" thực sự được gửi trong gói tin (có thể chứa mã độc). |
| **Gói tin** | Packet | Đơn vị dữ liệu nhỏ được truyền trên mạng. |
| **Luồng / Phiên** | Flow / Session | Chuỗi gói tin giữa hai bên trong một khoảng thời gian. |
| **Giao thức** | Protocol | Quy tắc truyền thông: `TCP`, `UDP`, `ICMP`… |
| **Dịch vụ / Cổng** | Service / Port | Dịch vụ mạng đang chạy, ví dụ `http` (80), `ftp` (21), `smtp` (25). |
| **Cờ TCP** | TCP flag | Trạng thái kết nối TCP, ví dụ `SF` (kết thúc bình thường), `S0` (không phản hồi), `REJ` (bị từ chối). |
| **Lưu lượng** | Traffic | Toàn bộ dữ liệu chạy qua mạng. |

---

## 2. Dữ liệu & tiền xử lý

| Thuật ngữ | English | Giải thích |
|---|---|---|
| **Đặc trưng** | Feature | Một biến đầu vào mô tả dữ liệu (ở đây là 41 đặc trưng của một kết nối). |
| **Nhãn** | Label | Kết quả đúng của mẫu, ví dụ `normal`, `neptune`. |
| **Lớp** | Class | Nhóm mà mẫu thuộc về (`Normal`, `DoS`, `Probe`, `R2L`, `U2R`). |
| **Biến phân loại** | Categorical variable | Biến nhận giá trị rời rạc dạng chữ: `protocol_type`, `service`, `flag`. |
| **Biến số** | Numerical variable | Biến nhận giá trị số: `src_bytes`, `duration`, `count`… |
| **One-hot encoding** | One-hot encoding | Biến một biến phân loại thành nhiều cột 0/1. Ví dụ `tcp/udp/icmp` → 3 cột. |
| **Label encoding** | Label encoding | Gán mỗi giá trị chữ thành một số nguyên (0, 1, 2…). Gọn nhưng tạo thứ tự giả. |
| **Chuẩn hóa Z-score** | Standardization | Đưa biến về trung bình 0, độ lệch chuẩn 1: `z = (x − μ) / σ`. |
| **Chuẩn hóa Min–Max** | Normalization | Đưa biến về khoảng [0, 1]: `x' = (x − min) / (max − min)`. |
| **Rò rỉ dữ liệu** | Data leakage | Dùng thông tin từ test (hoặc tương lai) khi train → kết quả đẹp giả tạo. Tránh bằng cách chỉ `fit` trên train. |
| **Mất cân bằng lớp** | Class imbalance | Số mẫu giữa các lớp chênh lệch lớn (U2R chỉ 52 mẫu so với DoS 45.927). |
| **Độ đa dạng giá trị** | Cardinality | Số giá trị khác nhau của một biến (`service` có 70 giá trị). |
| **Feature hằng** | Constant feature | Biến chỉ có một giá trị duy nhất (`num_outbound_cmds` toàn 0) → vô dụng, nên bỏ. |
| **Trùng lặp** | Duplicate | Hai dòng dữ liệu giống hệt nhau. NSL-KDD đã khử sẵn. |
| **Tập huấn luyện** | Training set | Dữ liệu dùng để học mô hình. |
| **Tập kiểm thử** | Test set | Dữ liệu chỉ dùng để đánh giá, không được học. |

---

## 3. Học máy

| Thuật ngữ | English | Giải thích |
|---|---|---|
| **Học có giám sát** | Supervised learning | Học từ dữ liệu **có nhãn** (biết trước normal/attack). |
| **Học không giám sát** | Unsupervised learning | Học từ dữ liệu **không có nhãn**, tự tìm cấu trúc. |
| **Học bán giám sát** | Semi-supervised learning | Dùng ít nhãn + nhiều dữ liệu chưa nhãn. |
| **Phân loại** | Classification | Dự đoán mẫu thuộc lớp nào (có nhãn khi học). |
| **Phân cụm** | Clustering | Gom mẫu giống nhau thành nhóm (không cần nhãn). |
| **Phát hiện dị biệt** | Anomaly detection | Tìm mẫu khác biệt so với số đông. |
| **Phát hiện cái mới** | Novelty detection | Khi train chỉ có dữ liệu "bình thường", phát hiện mẫu mới lạ khi dự đoán. |
| **Ngưỡng** | Threshold | Mức cắt để biến điểm số dị biệt thành nhãn (ví dụ điểm > ngưỡng → Attack). |
| **Siêu tham số** | Hyperparameter | Tham số phải chọn trước khi train (ví dụ `k` của K-Means, `eps` của DBSCAN). |
| **Mô hình cơ sở** | Baseline | Mô hình đơn giản dùng để so sánh (ví dụ Logistic Regression, Random Forest). |
| **Quá khớp** | Overfitting | Mô hình học thuộc train nhưng kém trên dữ liệu mới. |
| **Tổng quát hóa** | Generalization | Khả năng làm tốt trên dữ liệu chưa thấy. |
| **Hạt giống ngẫu nhiên** | Random seed / `random_state` | Cố định để kết quả tái lập được giữa các lần chạy. |

---

## 4. Phân cụm (Clustering)

| Thuật ngữ | English | Giải thích |
|---|---|---|
| **K-Means** | K-Means | Chia dữ liệu thành `k` cụm, lặp: gán điểm về tâm gần nhất → cập nhật tâm. |
| **Tâm cụm** | Centroid | Trung bình các điểm trong cụm; dùng để đo độ xa của điểm mới. |
| **Inertia / SSE** | Inertia / Sum of Squared Errors | Tổng bình phương khoảng cách từ điểm tới tâm cụm; càng nhỏ càng "chặt". |
| **Phương pháp khuỷu tay** | Elbow method | Vẽ inertia theo `k`, chọn `k` tại chỗ đường cong "gãy" (khuỷu). |
| **Điểm silhouette** | Silhouette score | Đo mức tách biệt của cụm (−1 → 1); càng cao càng tốt. |
| **DBSCAN** | Density-Based Spatial Clustering of Applications with Noise | Gom cụm theo **mật độ**; điểm lẻ bị coi là nhiễu. |
| **eps (ε)** | Epsilon | Bán kính lân cận trong DBSCAN. |
| **minPts** | Minimum points | Số điểm tối thiểu trong bán kính `eps` để thành vùng "đậm". |
| **Điểm lõi** | Core point | Điểm có đủ `minPts` hàng xóm trong bán kính `eps`. |
| **Điểm biên** | Border point | Không đủ hàng xóm nhưng nằm trong vùng của điểm lõi. |
| **Điểm nhiễu** | Noise point | Không thuộc cụm nào → **ứng viên dị biệt**. |
| **Mật độ** | Density | Mức tập trung các điểm trong một vùng không gian. |

---

## 5. Độ đo khoảng cách (Distance)

| Thuật ngữ | English | Giải thích |
|---|---|---|
| **Euclidean** | Euclidean distance | Khoảng cách đường thẳng quen thuộc; coi các chiều độc lập và **nhạy với thang đo**. |
| **Manhattan** | Manhattan distance | Tổng chênh lệch theo từng chiều (đi theo "đường phố"). |
| **Mahalanobis** | Mahalanobis distance | Khoảng cách có tính **phương sai và tương quan** giữa các chiều. |
| **Hiệp phương sai** | Covariance | Mức độ hai biến cùng biến thiên; dương = cùng tăng, âm = ngược nhau. |
| **Ma trận hiệp phương sai** | Covariance matrix (`Σ`) | Ma trận mô tả phương sai từng chiều và tương quan giữa mọi cặp chiều. |
| **Nghịch đảo ma trận** | Matrix inverse (`Σ⁻¹`) | Dùng trong Mahalanobis để "khử" tương quan và chuẩn hóa theo phương sai. |
| **Ma trận suy biến** | Singular matrix | Không nghịch đảo được (do feature hằng/đa cộng tuyến). |
| **Pseudo-inverse** | Moore–Penrose pseudo-inverse | "Nghịch đảo thay thế" khi ma trận suy biến. |
| **Chính quy hóa** | Regularization | Thêm một lượng nhỏ vào đường chéo `Σ` để tránh suy biến (ví dụ `Σ + λI`). |
| **Đa cộng tuyến** | Multicollinearity | Nhiều biến gần như phụ thuộc tuyến tính vào nhau. |

**Công thức**

```text
Euclidean:   d(x, y) = sqrt( Σ_i (x_i − y_i)² )

Mahalanobis: d(x, μ) = sqrt( (x − μ)ᵀ · Σ⁻¹ · (x − μ) )
```

> Trực giác: Euclidean hỏi *"cách xa bao nhiêu theo đường chim bay?"*;
> Mahalanobis hỏi *"lệch bao nhiêu **so với mức biến động bình thường** của từng chiều?"* → công bằng hơn với dữ liệu nhiều chiều.

---

## 6. Đánh giá mô hình (Evaluation)

| Thuật ngữ | English | Giải thích |
|---|---|---|
| **Ma trận nhầm lẫn** | Confusion matrix | Bảng đếm TP/TN/FP/FN giữa nhãn thật và dự đoán. |
| **TP** | True Positive | Dự đoán Attack, thực tế Attack. |
| **TN** | True Negative | Dự đoán Normal, thực tế Normal. |
| **FP** | False Positive | Dự đoán Attack, thực tế Normal (**báo nhầm**). |
| **FN** | False Negative | Dự đoán Normal, thực tế Attack (**bỏ sót**). |
| **Accuracy** | Accuracy | Tỉ lệ dự đoán đúng trên toàn bộ. **Dễ đánh lừa khi lệch lớp.** |
| **Precision** | Precision | Trong các ca báo Attack, bao nhiêu % đúng. |
| **Recall** | Recall / True Positive Rate | Trong các ca Attack thật, bắt được bao nhiêu %. |
| **F1-score** | F1-score | Trung bình điều hòa của Precision và Recall. |
| **FPR** | False Positive Rate | Tỉ lệ báo nhầm trên các ca Normal thật. |
| **ROC curve** | Receiver Operating Characteristic | Đường cong TPR theo FPR khi đổi ngưỡng. |
| **AUC** | Area Under the ROC Curve | Diện tích dưới ROC (0.5 = đoán mò, 1 = hoàn hảo). |
| **PR curve** | Precision–Recall curve | Đường cong Precision theo Recall. |
| **PR-AUC** | Area Under the PR Curve | Hợp hơn ROC-AUC khi dữ liệu **lệch lớp** (như bài này). |
| **Macro / Micro average** | Macro / Micro averaging | Cách trung bình điểm qua nhiều lớp (macro = trung bình đều, micro = gộp mẫu). |
| **Cross-validation** | Cross-validation | Chia dữ liệu nhiều phần để đánh giá ổn định hơn. |
| **Stratified split** | Stratified split | Chia dữ liệu giữ nguyên tỉ lệ lớp (quan trọng với U2R hiếm). |

**Công thức**

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 · Precision · Recall / (Precision + Recall)
Accuracy  = (TP + TN) / (TP + TN + FP + FN)
FPR       = FP / (FP + TN)
```

---

## 7. Thuật ngữ riêng của NSL-KDD

| Thuật ngữ | Giải thích |
|---|---|
| **KDD Cup 99** | Bộ dữ liệu phát hiện xâm nhập kinh điển (1999), nguồn gốc của NSL-KDD. |
| **NSL-KDD** | Bản **làm sạch** của KDD'99: bỏ bản ghi trùng lặp, giảm thiên lệch. |
| **`KDDTrain+`** | Tập huấn luyện đầy đủ: 125.973 dòng, 43 cột. |
| **`KDDTest+`** | Tập kiểm thử đầy đủ: 22.544 dòng, 43 cột; chứa cả tấn công **mới**. |
| **`KDDTrain+_20Percent`** | Bản rút gọn 20% của tập train. |
| **`KDDTest-21`** | Tập test đã **loại các bản ghi có difficulty = 21** (mức khó nhất). |
| **`.arff` vs `.txt`** | `.arff` = bản nhãn nhị phân `{normal, anomaly}`; `.txt` = nhãn tấn công cụ thể + difficulty. |
| **`difficulty`** | Điểm độ khó (1–21) của mẫu; **không dùng làm đặc trưng**, phải drop. |
| **Nhãn 5 lớp** | `Normal`, `DoS`, `Probe`, `R2L`, `U2R`. |
| **41 đặc trưng, 4 nhóm** | Basic (9) · Content (13) · Time-based traffic (9) · Host-based traffic (10). |
| **Feature hằng** | `num_outbound_cmds` toàn 0 → loại bỏ. |
| **Bản ghi dư thừa** | Redundant records — đã được khử trong NSL-KDD (bản KDD'99 gốc thì chưa). |

---

## Xem thêm

- [01 — Phân tích đề tài](./01-phan-tich-de-tai.md)
- Scikit-learn glossary: <https://scikit-learn.org/stable/glossary.html>
- NSL-KDD trên Kaggle: <https://www.kaggle.com/datasets/hassan06/nslkdd>
