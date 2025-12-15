from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
books = [
    {"id": 1, "title": "Python Basics", "author": "John Doe", "year": 2021},
    {"id": 2, "title": "Flask Guide", "author": "Jane Smith", "year": 2022}
]


def find_book(book_id):
    """
    Find a book by its ID.
    """
    return next((book for book in books if book["id"] == book_id), None)


def is_valid_book_data(data):
    """
    Validate incoming book data.
    """
    return (
        data
        and "title" in data
        and "author" in data
        and "year" in data
    )


@app.route("/", methods=["GET"])
def home():
    """
    Home route to check API status.
    """
    return jsonify({"message": "Library REST API is running"})


@app.route("/books", methods=["GET"])
def get_all_books():
    """
    Get all books.
    """
    return jsonify({"books": books})


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):
    """
    Get a single book by ID.
    """
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


@app.route("/books", methods=["POST"])
def add_book():
    """
    Add a new book.
    """
    data = request.get_json()

    if not is_valid_book_data(data):
        return jsonify({"error": "Invalid book data"}), 400

    new_book = {
        "id": books[-1]["id"] + 1 if books else 1,
        "title": data["title"],
        "author": data["author"],
        "year": data["year"]
    }

    books.append(new_book)
    return jsonify(new_book), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    """
    Update an existing book.
    """
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    if not is_valid_book_data(data):
        return jsonify({"error": "Invalid book data"}), 400

    book.update({
        "title": data["title"],
        "author": data["author"],
        "year": data["year"]
    })

    return jsonify(book)


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    """
    Delete a book.
    """
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    books.remove(book)
    return jsonify({"message": "Book deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
