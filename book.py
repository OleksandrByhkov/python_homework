from flask import Flask, render_template

app = Flask(__name__)

books = [
    {
        "title": "Шахрайство",
        "author": "Зеді Сміт",
        "category": "Художня література"
    },
    {
        "title": "Небаченні бактерії",
        "author": "Стів Молд",
        "category": "Книжки для дітей"
    },
    {
        "title": "Як це - бути собакою",
        "author": "Грегорі Бернз",
        "category": "Енциклопедія"
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/books")
def show_books():
    return render_template("books.html", books=books)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)