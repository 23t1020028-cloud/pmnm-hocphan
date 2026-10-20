from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    errors = {}
    result = None
    color_class = "success"
    h_val, w_val = "", ""

    if request.method == "POST":
        # 1. Lấy dữ liệu từ Form
        h_val = request.form.get("height", "").strip()
        w_val = request.form.get("weight", "").strip()

        h_num, w_num = None, None

        # 2. Kiểm tra ô Chiều cao (50 - 250 cm)
        if not h_val:
            errors["height"] = "Vui lòng nhập một số."
        else:
            try:
                h_num = float(h_val.replace(",", "."))
                # Cảnh báo riêng nếu người dùng nhập theo đơn vị mét 
                if 0.5 <= h_num <= 2.5:
                    errors["height"] = (
                        "Giá trị phải từ 50 đến 250. (nhập mét thay vì cm)"
                    )
                elif h_num < 50 or h_num > 250:
                    errors["height"] = "Giá trị phải từ 50 đến 250."
            except ValueError:
                errors["height"] = "Vui lòng nhập một số."

        # 3. Kiểm tra ô Cân nặng 
        if not w_val:
            errors["weight"] = "Vui lòng nhập một số."
        else:
            try:
                w_num = float(w_val.replace(",", "."))
                if w_num < 10 or w_num > 300:
                    errors["weight"] = "Giá trị phải từ 10 đến 300."
            except ValueError:
                errors["weight"] = "Vui lòng nhập một số."

        # 4. Tính toán kết quả khi không có lỗi
        if not errors:
            h_m = h_num / 100.0  # Đổi cm sang mét
            bmi = round(w_num / (h_m**2), 1)

            # Tính khoảng cân nặng nên có ứng với BMI 18.5 - 22.9
            min_w = round(18.5 * (h_m**2), 1)
            max_w = round(22.9 * (h_m**2), 1)

            # Phân loại theo chuẩn Châu Á & gán màu sắc
            if bmi < 18.5:
                category = "Thiếu cân"
                color_class = "warning"  # Màu vàng
            elif bmi < 23.0:
                category = "Bình thường"
                color_class = "success"  # Màu xanh
            elif bmi < 25.0:
                category = "Thừa cân"
                color_class = "warning"  # Màu vàng
            else:
                category = "Béo phì"
                color_class = "danger"  # Màu đỏ
    
            # Định dạng chuỗi thông báo kết quả
            if category == "Bình thường":
                result = f"{bmi} - {category}"

    return render_template(
        "index.html",
        errors=errors,
        result=result,
        color_class=color_class,
        h_val=h_val,
        w_val=w_val,
    )


if __name__ == "__main__":
    app.run(debug=True)