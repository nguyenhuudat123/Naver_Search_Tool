# Naver SEO Automation Helper (Semi-Auto)

## 📌 Giới thiệu
Đây là một công cụ hỗ trợ theo dõi thứ hạng từ khóa trên Naver (Search Engine lớn nhất Hàn Quốc). Dự án được phát triển để giải quyết các tác vụ thủ công lặp đi lặp lại trong quy trình làm báo cáo SEO hàng ngày.

**Hiệu quả thực tế:** Giảm 70% thời gian kiểm tra thủ công cho đội ngũ Digital Marketing.

## ✨ Tính năng chính
- **Keyword Generator**: Tự động kết hợp các thành phần (Địa chỉ + Món ăn + Đặc điểm) để tạo danh sách hàng trăm từ khóa SEO chỉ trong 1 lần nhập.
- **Auto Tab Management**: Tự động mở và quản lý nhiều tab trình duyệt, điều hướng trực tiếp đến trang kết quả tìm kiếm của Naver.
- **Smart Target Highlighting**: Tự động tìm kiếm thương hiệu mục tiêu trong trang, cuộn đến vị trí đó và đánh dấu (Highlight) để người dùng dễ dàng nhận diện.
- **Semi-Auto Workflow**: Tự động đóng các tab không tìm thấy kết quả để tiết kiệm tài nguyên máy tính (RAM/CPU) và giữ lại các tab có kết quả để đối soát thủ công.
- **Pause/Resume/Stop**: Cho phép tạm dừng quá trình quét để kiểm tra và tiếp tục bất cứ lúc nào.

## 🛠 Công nghệ sử dụng
- **Ngôn ngữ**: Python
- **Thư viện chính**: 
  - `Selenium`: Tự động hóa trình duyệt.
  - `Tkinter`: Xây dựng giao diện người dùng (GUI).
  - `Threading`: Xử lý đa luồng giúp giao diện không bị treo khi đang quét web.
  - `WebDriver Manager`: Tự động cập nhật Driver phù hợp với phiên bản Chrome hiện tại.

## 🚀 Hướng dẫn cài đặt
1. Tải bộ mã nguồn về máy.
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt