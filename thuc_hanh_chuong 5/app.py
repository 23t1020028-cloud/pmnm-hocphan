from flask import Flask, render_template, request, session, flash, redirect, url_for
from forms import RegisterForm
app = Flask(__name__)

USERS = {
    "admin": "admin123",
    "an": "an123456"
}

app.secret_key = "thb_flask_secret_key_123"

#  MÁY TÍNH CƠ BẢN 
@app.route("/", methods=["GET", "POST"])
@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    errors = {}
    result = None
    a_val, b_val, op = "", "", "+"

    if request.method == "POST":
        a_val = request.form.get("a", "").strip()
        op = request.form.get("op", "+").strip()
        b_val = request.form.get("b", "").strip()

        a_num, b_num = None, None

        if not a_val:
            errors["a"] = "Vui lòng nhập một số."
        else:
            try:
                a_num = float(a_val.replace(",", "."))
            except ValueError:
                errors["a"] = "Vui lòng nhập một số."

        if not b_val:
            errors["b"] = "Vui lòng nhập một số."
        else:
            try:
                b_num = float(b_val.replace(",", "."))
            except ValueError:
                errors["b"] = "Vui lòng nhập một số."

        if op not in ["+", "-", "*", "/"]:
            errors["op"] = "Phép toán không hợp lệ."

        if op == "/" and b_num == 0:
            errors["b"] = "Không thể chia cho 0."

        if not errors:
            if op == "+":
                res = a_num + b_num
            elif op == "-":
                res = a_num - b_num
            elif op == "*":
                res = a_num * b_num
            elif op == "/":
                res = a_num / b_num

            def fmt(n):
                return int(n) if n.is_integer() else n

            result = f"{fmt(a_num)} {op} {fmt(b_num)} = {fmt(res)}"

    return render_template(
        "calculator.html",
        errors=errors,
        result=result,
        a_val=a_val,
        b_val=b_val,
        op=op,
    )


# TÍNH ĐIỂM HỌC PHẦN 
def validate_score(val_str):
    if not val_str:
        return None, "Vui lòng nhập một số."
    val_str = val_str.replace(",", ".")
    try:
        score = float(val_str)
        if score < 0 or score > 10:
            return None, "Điểm phải từ 0 đến 10"
        return score, None
    except ValueError:
        return None, "Vui lòng nhập một số."


@app.route("/sodiem", methods=["GET", "POST"])
def sodiem():
    errors = {}
    result = None
    cc_val, gk_val, ck_val = "", "", ""

    if request.method == "POST":
        cc_val = request.form.get("cc", "").strip()
        gk_val = request.form.get("gk", "").strip()
        ck_val = request.form.get("ck", "").strip()

        cc_num, errors["cc"] = validate_score(cc_val)
        gk_num, errors["gk"] = validate_score(gk_val)
        ck_num, errors["ck"] = validate_score(ck_val)

        errors = {k: v for k, v in errors.items() if v}

        if not errors:
            overall = round(cc_num * 0.1 + gk_num * 0.3 + ck_num * 0.6, 1)

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
        "sodiem.html",
        errors=errors,
        result=result,
        cc_val=cc_val,
        gk_val=gk_val,
        ck_val=ck_val,
    )


#  TÍNH BMI 
@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    errors = {}
    result = None
    color_class = "success"
    h_val, w_val = "", ""

    if request.method == "POST":
        h_val = request.form.get("height", "").strip()
        w_val = request.form.get("weight", "").strip()

        h_num, w_num = None, None

        if not h_val:
            errors["height"] = "Vui lòng nhập một số."
        else:
            try:
                h_num = float(h_val.replace(",", "."))
                if 0.5 <= h_num <= 2.5:
                    errors["height"] = (
                        "Giá trị phải từ 50 đến 250. (nhập mét thay vì cm)"
                    )
                elif h_num < 50 or h_num > 250:
                    errors["height"] = "Giá trị phải từ 50 đến 250."
            except ValueError:
                errors["height"] = "Vui lòng nhập một số."

        if not w_val:
            errors["weight"] = "Vui lòng nhập một số."
        else:
            try:
                w_num = float(w_val.replace(",", "."))
                if w_num < 10 or w_num > 300:
                    errors["weight"] = "Giá trị phải từ 10 đến 300."
            except ValueError:
                errors["weight"] = "Vui lòng nhập một số."

        if not errors:
            h_m = h_num / 100.0
            bmi_val = round(w_num / (h_m**2), 1)

            min_w = round(18.5 * (h_m**2), 1)
            max_w = round(22.9 * (h_m**2), 1)

            if bmi_val < 18.5:
                category = "Thiếu cân"
                color_class = "warning"
            elif bmi_val < 23.0:
                category = "Bình thường"
                color_class = "success"
            elif bmi_val < 25.0:
                category = "Thừa cân"
                color_class = "warning"
            else:
                category = "Béo phì"
                color_class = "danger"

            if category == "Bình thường":
                result = (
                    f"{bmi_val} - {category}; nên có {min_w} - {max_w} kg"
                )
            else:
                result = f"{bmi_val} - {category}"

    return render_template(
        "bmi.html",
        errors=errors,
        result=result,
        color_class=color_class,
        h_val=h_val,
        w_val=w_val,
    )

# ĐĂNG NHẬP
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("profile"))

    username = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember")

        if username in USERS and USERS[username] == password:
            session["user"] = username
            if remember:
                session.permanent = True  
            flash(
                f"Xin chào {username} đã đăng nhập thành công !",
                "success",
            )
            return redirect(url_for("profile"))
        else:
            flash("Sai tên đăng nhập hoặc mật khẩu.", "danger")

    return render_template("login.html", username=username)

# PROFILE
@app.route("/profile")
def profile():
    if "user" not in session:
        flash("Vui lòng đăng nhập...", "warning")
        return redirect(url_for("login"))

    return render_template("profile.html")

# LOGOUT
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for("login"))

# RESGITER
@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect(url_for("profile"))

    form = RegisterForm(users_dict=USERS)

    if form.validate_on_submit():
        new_username = form.username.data.strip()
        new_password = form.password.data

        USERS[new_username] = new_password

        flash("Đăng ký thành công.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)