from datetime import date
from flask import Flask, abort, jsonify, render_template, request

app = Flask(__name__)

# Cơ sở dữ liệu mẫu
BOOKS = [
    {
        "id": 1,
        "title": "Lập trình Python cơ bản",
        "author": "Nguyễn Văn A",
        "category": "Công nghệ",
        "pub_year": 2023,
        "available": True,
        "desc": "Sách hướng dẫn lập trình Python từ căn bản đến nâng cao.",
    },
    {
        "id": 2,
        "title": "Thiết kế CSDL SQL",
        "author": "Trần Thị B",
        "category": "Công nghệ",
        "pub_year": 2022,
        "available": False,
        "desc": "Kiến thức về chuẩn hóa và thiết kế CSDL quan hệ.",
    },
    {
        "id": 3,
        "title": "Học Flask qua dự án",
        "author": "Lê Văn C",
        "category": "Công nghệ",
        "pub_year": 2024,
        "available": True,
        "desc": "Thực hành xây dựng ứng dụng Web Flask thực tế.",
    },
    {
        "id": 4,
        "title": "Đắc Nhân Tâm",
        "author": "Dale Carnegie",
        "category": "Kỹ năng",
        "pub_year": 2021,
        "available": True,
        "desc": "Nghệ thuật thu phục lòng người và giao tiếp.",
    },
    {
        "id": 5,
        "title": "Lịch sử Thế giới",
        "author": "Phạm Văn D",
        "category": "Lịch sử",
        "pub_year": 2020,
        "available": False,
        "desc": "Tổng quan về các nền văn minh lớn trong lịch sử.",
    },
]


# Context Processor: Tự động truyền danh sách thể loại & năm hiện tại
@app.context_processor
def inject_globals():
    categories = sorted(list(set(book["category"] for book in BOOKS)))
    return {"all_categories": categories, "current_year": date.today().year}


# 1. Trang chủ
@app.route("/")
def home():
    total_books = len(BOOKS)
    available_books = sum(1 for b in BOOKS if b["available"])
    # Lấy 3 sách xuất bản gần đây nhất
    recent_books = sorted(BOOKS, key=lambda x: x["pub_year"], reverse=True)[:3]

    return render_template(
        "index.html",
        total_books=total_books,
        available_books=available_books,
        recent_books=recent_books,
    )


# 2. Trang danh sách sách & lọc theo thể loại
@app.route("/books")
def books():
    category_filter = request.args.get("category", "").strip()

    if category_filter:
        filtered_books = [
            b for b in BOOKS if b["category"].lower() == category_filter.lower()
        ]
    else:
        filtered_books = BOOKS

    return render_template(
        "books.html", books=filtered_books, selected_category=category_filter
    )


# 3. Trang chi tiết sách
@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        abort(
            404, description=f"Không tìm thấy cuốn sách có mã số ID = {book_id}"
        )

    return render_template("book_detail.html", book=book)


# 4. REST API (Giữ nguyên, trả về JSON)
@app.route("/api/books", methods=["GET"])
def api_books():
    return jsonify(BOOKS)


@app.route("/api/books/<int:book_id>", methods=["GET"])
def api_book_detail(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


# 5. Xử lý lỗi 404 bằng Template
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", message=error.description), 404


if __name__ == "__main__":
    app.run(debug=True)