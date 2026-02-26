# Naver SEO Pro - Search Automation & Logging

## 📌 Giới thiệu
Naver SEO Pro là công cụ tự động hóa thao tác kiểm tra thứ hạng từ khóa trên công cụ tìm kiếm Naver. Phiên bản nâng cấp được thiết kế lại logic xử lý tổ hợp dữ liệu và tích hợp hệ thống quản lý nhật ký (log) cục bộ, giúp chuẩn hóa quy trình báo cáo SEO và tối ưu hóa việc đối soát kết quả thủ công.

## ✨ Tính năng chính
- **Brute-force Keyword Engine**: Sử dụng thuật toán tích Đề-các (`itertools.product`) để tự động tạo danh sách tổ hợp từ khóa từ 6 biến số đầu vào linh hoạt (Địa chỉ chính, Địa chỉ phụ, Món ăn, và 3 trường Đặc điểm tùy chọn).
- **Campaign Metadata Tracking**: Cung cấp khu vực khai báo siêu dữ liệu chiến dịch (Target Link, Header Name, Option/Note) để gán nhãn cho từng luồng kiểm tra.
- **Automated CSV Logging**: Tự động khởi tạo hệ thống thư mục `SearchLog/` theo ngày. Hỗ trợ ghi lại toàn bộ trạng thái hệ thống (Snapshot), nhật ký hoạt động (System Log) và lưu trữ kết quả kết xuất (kể cả kết quả chỉnh sửa thủ công) dưới định dạng tệp `.csv`.
- **Smart Tab Management & Target Highlighting**: Điều khiển luồng Chrome độc lập, tự động cuộn trang, đóng khung đỏ (highlight) thương hiệu mục tiêu. Hệ thống tự động đóng các tab không chứa kết quả để giải phóng bộ nhớ (RAM).
- **Asynchronous Execution Control**: Quản lý tiến trình quét bằng đa luồng (Threading), cho phép can thiệp thời gian thực qua các lệnh Start, Pause, Resume và Stop mà không gây đóng băng giao diện người dùng.

## 🛠 Công nghệ sử dụng
- **Ngôn ngữ**: Python 3.x
- **Thư viện cốt lõi**:
  - `selenium` & `webdriver-manager`: Tự động hóa thao tác trình duyệt và tự động cập nhật ChromeDriver.
  - `tkinter`: Khung giao diện đồ họa (GUI).
  - `threading`: Xử lý tác vụ nền.
  - `csv`, `os`, `itertools`: Quản lý luồng tệp tin, xử lý tổ hợp mảng và trích xuất dữ liệu (Thư viện tiêu chuẩn của Python).

## 🚀 Hướng dẫn cài đặt
1. Tải toàn bộ mã nguồn về môi trường cục bộ.
2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
