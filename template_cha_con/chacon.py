from datetime import date
from flask import Flask, render_template

app = Flask(__name__)


# Context processor (Trang 41)
@app.context_processor
def inject_globals():
    return {
        "site_name": "Website Cá Nhân",
        "author_name": "Tô Hữu Bằng",
        "current_year": date.today().year,
    }


# Chỉ dùng 1 hàm about() cho cả 2 route / và /about
@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/hoc-van")
def hoc_van():
    return render_template("hoc_van.html")


@app.route("/du-an")
def du_an():
    ds_du_an = [
        {"name": "MiniBlog v0.2", "desc": "Ứng dụng blog bằng Flask & Jinja2"},
        {"name": "LibraryMS v0.2", "desc": "Hệ thống quản lý thư viện"},
    ]
    return render_template("du_an.html", projects=ds_du_an)


@app.route("/lien-he")
def lien_he():
    return render_template("lien_he.html")


if __name__ == "__main__":
    app.run(debug=True)