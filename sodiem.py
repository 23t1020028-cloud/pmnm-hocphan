from flask import Flask, jsonify, request, abort, redirect, make_response
import html

app = Flask(__name__)

STUDENTS = {
    "23T102001": {"name": "Nguyễn Văn An", "lop": "K47A", "scores": {"PMMNM": 8.5, "CSDL": 7.0, "LTMT": 9.0}},
    "23T102002": {"name": "Trần Thị Bình", "lop": "K47A", "scores": {"PMMNM": 6.0, "CSDL": 5.5, "LTMT": 7.0}},
    "23T102003": {"name": "Lê Hoàng Cường", "lop": "K47B", "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T102004": {"name": "Phạm Minh Dũng", "lop": "K47B", "scores": {"PMMNM": 4.0, "CSDL": 3.5, "LTMT": 5.0}},
    "23T102005": {"name": "Hoàng Thu Hà", "lop": "K47A", "scores": {}},
    "23T102006": {"name": "Võ Quốc Khánh", "lop": "K47C", "scores": {"PMMNM": 7.5, "LTMT": 9.0}}
}

# --- CÂU 1 ---
@app.route("/")
def home():
    lops = sorted(list(set(s["lop"] for s in STUDENTS.values())))
    return f"<h2>Trang chủ</h2><p>Tổng SV: {len(STUDENTS)}</p><p>Số lớp: {len(lops)} ({', '.join(lops)})</p><a href='/students'>Danh sách</a> | <a href='/search'>Tìm kiếm</a>"

@app.route("/api/students")
def api_students():
    return jsonify(STUDENTS)

# --- CÂU 2 ---
@app.route("/students")
def list_students():
    lop = request.args.get("lop", "").strip()
    rows = ""
    for m, s in STUDENTS.items():
        if not lop or s["lop"].upper() == lop.upper():
            d = s["scores"].values()
            dtb = f"{sum(d)/len(d):.2f}" if d else "-"
            xl = "Giỏi" if d and sum(d)/len(d)>=8.0 else "Khá/TB" if d else "Chưa có"
            rows += f"<tr><td><a href='/students/{m}'>{m}</a></td><td>{s['name']}</td><td>{s['lop']}</td><td>{dtb}</td><td>{xl}</td></tr>"
    return f"<table border='1'><tr><th>MSSV</th><th>Họ tên</th><th>Lớp</th><th>ĐTB</th><th>XL</th></tr>{rows}</table>"

# --- CÂU 3 ---
@app.route("/students/<mssv>")
def student_detail(mssv):
    s = STUDENTS.get(mssv)
    if not s:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    
    d = s["scores"].values()
    dtb = f"{sum(d)/len(d):.2f}" if d else "-"
    diem_html = "".join([f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in s["scores"].items()])
    
    return f"""
    <h2>Chi tiết: {s['name']} ({mssv})</h2>
    <p>Lớp: <a href="/students?lop={s['lop']}">{s['lop']}</a> | ĐTB: {dtb}</p>
    <p>Link rút gọn: <a href="/sv/{mssv}">/sv/{mssv}</a> | <a href="/students/{mssv}/export">Tải CSV</a></p>
    <table border="1"><tr><th>Môn</th><th>Điểm</th></tr>{diem_html}</table>
    <br><a href="/students">← Quay lại</a>
    """

# --- CÂU 4 ---
@app.route("/sv/<mssv>")
def redirect_sv(mssv):
    return redirect(f"/students/{mssv}", code=301)

# --- CÂU 5 ---
@app.route("/students/<mssv>/export")
def export_csv(mssv):
    s = STUDENTS.get(mssv)
    if not s:
        abort(404)
    content = "hoc_phan,diem\n" + "\n".join([f"{k},{v}" for k, v in s["scores"].items()])
    res = make_response(content)
    res.headers["Content-Type"] = "text/csv; charset=utf-8"
    res.headers["Content-Disposition"] = f"attachment; filename=diem_{mssv}.csv"
    return res

# --- CÂU 6 ---
@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    q_safe = html.escape(q)
    res = [f"<li><a href='/students/{m}'>{html.escape(s['name'])} ({m})</a></li>" 
           for m, s in STUDENTS.items() if q and (q.lower() in s['name'].lower() or q.lower() in m.lower())]
    
    return f"""
    <form action="/search" method="GET">
        <input type="text" name="q" value="{q_safe}">
        <button type="submit">Tìm</button>
    </form>
    {"<p>Tìm thấy " + str(len(res)) + " kết quả cho '" + q_safe + "':</p><ul>" + "".join(res) + "</ul>" if q else ""}
    """

if __name__ == "__main__":
    app.run(debug=True, port=8000)