from flask import Flask, render_template, request

app = Flask(__name__)


# Hàm kiểm tra điểm dùng chung cho cả 3 ô (CC, GK, CK)
def validate_score(val_str):
    if not val_str:
        return None, "Vui lòng nhập một số."

    # Chấp nhận dấu phẩy thập phân (ví dụ 7,5 -> 7.5)
    val_str = val_str.replace(",", ".")

    try:
        score = float(val_str)
        if score < 0 or score > 10:
            return None, "Điểm phải từ 0 đến 10"
        return score, None
    except ValueError:
        return None, "Vui lòng nhập một số."


@app.route("/", methods=["GET", "POST"])
def index():
    errors = {}
    result = None
    cc_val, gk_val, ck_val = "", "", ""

    if request.method == "POST":
        # 1. Lấy dữ liệu từ Form
        cc_val = request.form.get("cc", "").strip()
        gk_val = request.form.get("gk", "").strip()
        ck_val = request.form.get("ck", "").strip()

        # 2. Sử dụng hàm dùng chung để validate cả 3 ô
        cc_num, errors["cc"] = validate_score(cc_val)
        gk_num, errors["gk"] = validate_score(gk_val)
        ck_num, errors["ck"] = validate_score(ck_val)

        # Lọc bỏ các ô không có lỗi
        errors = {k: v for k, v in errors.items() if v}

        # 3. Tính điểm nếu không có lỗi
        if not errors:
            # Điểm học phần = CC (10%) + GK (30%) + CK (60%)
            overall = round(cc_num * 0.1 + gk_num * 0.3 + ck_num * 0.6, 1)

            # Quy đổi điểm chữ (Xét điểm liệt CK < 1 trước)
            if ck_num < 1.0:
                grade_letter = "F (điểm thi dưới 1)"
            elif overall >= 8.5:
                grade_letter = "A"
            elif overall >= 7.0:
                grade_letter = "B"
            elif overall >= 5.5:
                grade_letter = "C"
            elif overall >= 4.0:
                grade_letter = "D"
            else:
                grade_letter = "F"

            result = f"{overall} - {grade_letter}"

    return render_template(
        'index.html',
        errors=errors,
        result=result,
        cc_val=cc_val,
        gk_val=gk_val,
        ck_val=ck_val,
    )


if __name__ == "__main__":
    app.run(debug=True)