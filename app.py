from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  

def get_db_connection():
    conn = sqlite3.connect("RecipeSite_Database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db_connection()
    recipes = conn.execute("SELECT * FROM Recipe").fetchall()
    conn.close()
    return render_template("index.html", recipes=recipes)



@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    conn = get_db_connection()
    
    recipe = conn.execute("SELECT * FROM Recipe WHERE RecipeID = ?", (recipe_id,)).fetchone()
   
    ingredients = conn.execute("""
        SELECT i.IngredientName, ir.Quantity, ir.Unit 
        FROM Ingredients i
        JOIN Ingredients_Recipe ir ON i.IngredientID = ir.IngredientID
        WHERE ir.RecipeID = ?
    """, (recipe_id,)).fetchall()
    
    conn.close()
    return render_template("recipe_detail.html", recipe=recipe, ingredients=ingredients)



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO Users (Username, Email, PasswordHash) VALUES (?, ?, ?)",
                (username, email, hashed_password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Username or email already exists."

        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM Users WHERE Username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["PasswordHash"], password):
            session["user_id"] = user["UserID"]
            session["username"] = user["Username"]
            return redirect(url_for("home"))
        else:
            return "Invalid username or password."

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)