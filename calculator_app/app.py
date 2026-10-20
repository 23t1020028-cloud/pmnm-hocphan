from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def calculator():
    errors = {}
    result = None
    a_val = ""
    b_val = ""
    op = "+"

    if request.method == "POST":
        # 1. Lấy dữ liệu từ Form
        a_val = request.form.get("a", "").strip()
        op = request.form.get("op", "+").strip()
        b_val = request.form.get("b", "").strip()

        a_num = None
        b_num = None

        # 2. Kiểm tra ô 'a'
        if not a_val:
            errors["a"] = "Vui lòng nhập một số."
        else:
            try:
                a_num = float(a_val.replace(",", "."))
            except ValueError:
                errors["a"] = "Vui lòng nhập một số."

        # 3. Kiểm tra ô 'b'
        if not b_val:
            errors["b"] = "Vui lòng nhập một số."
        else:
            try:
                b_num = float(b_val.replace(",", "."))
            except ValueError:
                errors["b"] = "Vui lòng nhập một số."

        # 4. Kiểm tra phép toán 'op' hợp lệ
        valid_ops = ["+", "-", "*", "/"]
        if op not in valid_ops:
            errors["op"] = "Phép toán không hợp lệ."

        # 5. Kiểm tra lỗi chia cho 0
        if op == "/" and b_num == 0:
            errors["b"] = "Không thể chia cho 0."

        # 6. Tính toán kết quả nếu không có bất kỳ lỗi nào
        if not errors:
            if op == "+":
                res = a_num + b_num
            elif op == "-":
                res = a_num - b_num
            elif op == "*":
                res = a_num * b_num
            elif op == "/":
                res = a_num / b_num

            # Hàm định dạng số gọn đẹp 
            def fmt(n):
                return int(n) if n.is_integer() else n

            result = f"{fmt(a_num)} {op} {fmt(b_num)} = {fmt(res)}"

    return render_template(
        "index.html",
        errors=errors,
        result=result,
        a_val=a_val,
        b_val=b_val,
        op=op,
    )


if __name__ == "__main__":
    app.run(debug=True)