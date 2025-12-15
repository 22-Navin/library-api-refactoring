from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database (list of books)
books = []
book_id = 1

# Home route
@app.route('/')
def home():
    return jsonify({
        "message": "Library REST API is running"
    })

# GET all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# GET a single book by ID
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    for book in books:
        if book['id'] == id:
            return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# ADD a new book
@app.route('/books', methods=['POST'])
def add_book():
    global book_id
    data = request.get_json()

    new_book = {
        "id": book_id,
        "title": data.get("title"),
        "author": data.get("author"),
        "year": data.get("year")
    }

    books.append(new_book)
    book_id += 1

    return jsonify(new_book), 201

# UPDATE a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()

    for book in books:
        if book['id'] == id:
            book['title'] = data.get("title", book['title'])
            book['author'] = data.get("author", book['author'])
            book['year'] = data.get("year", book['year'])
            return jsonify(book)

    return jsonify({"error": "Book not found"}), 404

# DELETE a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    for book in books:
        if book['id'] == id:
            books.remove(book)
            return jsonify({"message": "Book deleted successfully"})

    return jsonify({"error": "Book not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
