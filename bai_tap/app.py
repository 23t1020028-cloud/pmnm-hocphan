from flask import Flask, abort

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def hello():
    return "<h1>Hello, Tô Hữu Bằng - 23T1020028</h1>"

@app.route("/chia-nhom")
def chianhom():
    so_bai = 12
    so_nhom = 3
    return f"Mỗi nhóm làm {so_bai / so_nhom} bài"

@app.route("/user/<user_name>")
def user_profile(user_name):
    return f"Chào mừng {user_name} đến với trang cá nhân của bạn !"

@app.route("/square/<int:n>")
@app.route("/square/<float:n>")
def square(n):
    res = n ** 2
    return f"Bình phương của {n} là: {res}"

# Route xử lý nhận danh sách số nguyên cách nhau bằng dấu phẩy
@app.route("/sum/<raw_number>")
def sum_number(raw_number):
    try:
        numbers = [int(x) for x in raw_number.split(",")]
        return f"Danh sách các số: {numbers} - Tổng các số: {sum(numbers)}"
    except ValueError:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)
