from flask import Flask, render_template, request, redirect, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'hardcoded-key'
DB = 'database.db'

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT, password TEXT
            );
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, description TEXT, price REAL
            );
            CREATE TABLE reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER, author TEXT, content TEXT
            );
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT, product_id INTEGER, card_number TEXT
            );
        """)
        c.executemany("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", [
            ("Glitchy Sneakers", "Comfortably unstable. Inject style, not stability.", 59.99),
            ("Cyber Shades", "Look shady, feel shady. 100% opaque.", 29.99),
            ("404 Hoodie", "This hoodie doesn’t exist. But you can wear it.", 44.99),
        ])
        conn.commit()
        conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect(DB)
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("home.html", products=products)

@app.route('/product/<int:pid>', methods=["GET", "POST"])
def product(pid):
    conn = sqlite3.connect(DB)
    if request.method == "POST":
        author = request.form['author']
        content = request.form['content']
        conn.execute(f"INSERT INTO reviews (product_id, author, content) VALUES ({pid}, '{author}', '{content}')")
        conn.commit()

    product = conn.execute(f"SELECT * FROM products WHERE id = {pid}").fetchone()
    reviews = conn.execute(f"SELECT author, content FROM reviews WHERE product_id = {pid}").fetchall()
    conn.close()
    return render_template("product.html", product=product, reviews=reviews)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect(DB)
        conn.execute(f"INSERT INTO users (username, password) VALUES ('{user}', '{pwd}')")
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect(DB)
        result = conn.execute(f"SELECT * FROM users WHERE username = '{user}' AND password = '{pwd}'").fetchone()
        conn.close()
        if result:
            session['user'] = user
            return redirect('/')
    return render_template("login.html")

@app.route('/cart/add/<int:pid>')
def add_to_cart(pid):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(pid)
    return redirect('/cart')

@app.route('/cart')
def view_cart():
    conn = sqlite3.connect(DB)
    cart_items = []
    if 'cart' in session:
        for pid in session['cart']:
            product = conn.execute(f"SELECT * FROM products WHERE id = {pid}").fetchone()
            if product:
                cart_items.append(product)
    conn.close()
    return render_template("cart.html", items=cart_items)

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user' not in session: return redirect('/login')
    card = request.form['card']
    conn = sqlite3.connect(DB)
    for pid in session.get('cart', []):
        conn.execute(f"INSERT INTO orders (user, product_id, card_number) VALUES ('{session['user']}', {pid}, '{card}')")
    conn.commit()
    conn.close()
    session.pop('cart', None)
    return "✅ Order placed."

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB)
    reviews = conn.execute("SELECT * FROM reviews").fetchall()
    orders = conn.execute("SELECT * FROM orders").fetchall()
    conn.close()
    return render_template("admin.html", reviews=reviews, orders=orders)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

