Bài tập Nhỏ: Làm quen với Template Cha Con trong Flask

Đây là bài tập nhỏ nhằm làm quen với framework Flask, cách tổ chức cấu trúc dự án Web Python và tái sử dụng giao diện bằng Jinja2.

🎯 Các kỹ năng cần học & áp dụng

Để hoàn thành bài tập này, sinh viên cần nắm vững các kỹ năng sau:

Quản lý Môi trường Python (Environment & Tooling)

Tạo và kích hoạt môi trường ảo (python -m venv .venv).

Khắc phục lỗi quyền thi hành script trên Windows PowerShell (ExecutionPolicy).

Quản lý và cài đặt gói thư viện qua pip (requirements.txt).

Lập trình Backend với Flask Framework

Khởi tạo ứng dụng Flask cơ bản (app = Flask(__name__)).

Định nghĩa các tuyến đường (Routing) cho trang web (@app.route()).

Xử lý điều hướng trùng lặp (1 hàm xử lý cho nhiều route).

Truyền dữ liệu toàn cục cho mọi template thông qua @app.context_processor.

Cơ chế Jinja2 Templating

Kế thừa Template (Template Inheritance): Sử dụng thẻ {% extends %} và {% block %} để xây dựng trang con dựa trên base.html.

Tách Component: Dùng {% include %} để chia nhỏ thanh menu (_navbar.html) và chân trang (_footer.html).

Đánh dấu trang hiện tại: Kiểm tra request.endpoint để tự động highlight menu active.

Tùy chỉnh Giao diện (HTML/CSS & Bootstrap)

Tích hợp Bootstrap 5 cơ bản.

Sử dụng CSS Variables để thiết lập màu chủ đạo (Navbar Xanh Nhạt #e0f2fe, trạng thái Active/Brand màu Đỏ #ff4d4d).

Căn chỉnh Logo và khoảng cách responsive đơn giản.

Đóng gói & Triển khai (Git & Vercel)

Quản lý mã nguồn bằng Git (add, commit, push).

Viết cấu hình vercel.json để đưa ứng dụng Python/Flask lên Vercel Serverless.

🛠️ Hướng dẫn chạy nhanh

Chạy cục bộ:

python -m venv .venv
.\.venv\Scripts\Activate
pip install flask
cd template_cha_con
python chacon.py


Deploy Vercel: Push code lên GitHub, chọn Root Directory là template_cha_con khi Import vào Vercel.
Link Vercel: https://vercel.com/tony-1463/pmnm-hocphan
