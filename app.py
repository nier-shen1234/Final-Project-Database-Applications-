from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("RecipeSite_Database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db_connection()
    recipes = conn.execute("SELECT * FROM Recipe LIMIT 10").fetchall()
    conn.close()
    return render_template("index.html", recipes=recipes)

@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    conn = get_db_connection()
    recipe = conn.execute("SELECT * FROM Recipe WHERE id = ?", (recipe_id,)).fetchone()
    conn.close()
    return render_template("recipe_detail.html", recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True)