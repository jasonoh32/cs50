import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, printing, usd, breakfast, lunch, dinner

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    """Allow user to change password"""
    if request.method == "POST":

        # Ensure current password is not empty
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)

        # Query database for user_id
        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Ensure current password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("current_password")):
            return apology("invalid password", 400)

        # Ensure new password is not empty
        if not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Ensure new password confirmation is not empty
        elif not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation", 400)

        # Ensure new password and confirmation match
        elif request.form.get("new_password") != request.form.get("new_password_confirmation"):
            return apology("new password and confirmation must match", 400)

        # Update database
        hash = generate_password_hash(request.form.get("new_password"))
        rows = db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=session["user_id"], hash=hash)

        # Show flash
        flash("Changed!")

    return render_template("change_password.html")


@app.route("/")
@login_required
def index():

    """Show Meal Plan"""
    # Create totals of chart values
    protein_total = db.execute("SELECT SUM(protein) as totalprotein FROM history WHERE id = :user_id", user_id = session["user_id"])
    sodium_total = db.execute("SELECT SUM(sodium) as totalsodium FROM history WHERE id = :user_id", user_id = session["user_id"])
    sugar_total = db.execute("SELECT SUM(sugar) as totalsugar FROM history WHERE id = :user_id", user_id = session["user_id"])
    fat_total = db.execute("SELECT SUM(fat) as totalfat FROM history WHERE id = :user_id", user_id = session["user_id"])
    calories_total = db.execute("SELECT SUM(calories) as totalcalories FROM history WHERE id = :user_id", user_id = session["user_id"])
    carbs_total = db.execute("SELECT SUM(carbs) as totalcarbs FROM history WHERE id = :user_id", user_id = session["user_id"])
    cholesterol_total = db.execute("SELECT SUM(cholesterol) as totalcholesterol FROM history WHERE id = :user_id", user_id = session["user_id"])
    fiber_total = db.execute("SELECT SUM(fiber) as totalfiber FROM history WHERE id = :user_id", user_id = session["user_id"])

    # Select row in table to input into html file
    transactions = db.execute("SELECT * FROM history WHERE id = :user_id", user_id = session["user_id"])

    # Render html information
    return render_template("index.html", transactions = transactions,
    protein_total = protein_total[0]["totalprotein"],
    sodium_total = sodium_total[0]["totalsodium"],
    sugar_total = sugar_total[0]["totalsugar"],
    fat_total = fat_total[0]["totalfat"],
    calories_total = calories_total[0]["totalcalories"],
    carbs_total = carbs_total[0]["totalcarbs"],
    cholesterol_total = cholesterol_total[0]["totalcholesterol"],
    fiber_total = fiber_total[0]["totalfiber"])


@app.route("/menu", methods=["GET", "POST"])
@login_required
def menu():

    """Add food into meal plan"""
    if request.method == "POST":
        quote = lookup(request.form.get("id"))

        # Check if the symbol exists
        if not quote:
            return apology("No nutrional info found", 400)

        # Check if the shares specified was a positive integer
        try:
            servings = int(request.form.get("servings"))
        except:
            return apology("servings must be a positive integer", 400)

        # Check if the number of servings requested was 0 or not
        if servings <= 0:
            return apology("cannot add 0 or fewer servings", 400)

        # Query database for history
        more = db.execute("SELECT servings FROM history WHERE id = :user_id AND food = :food", user_id = session["user_id"], food = quote["food"])
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # If first time adding food
        if not more:
            db.execute("INSERT INTO history (food, servings, id, date, protein, sodium, sugar, fat, calories, cholesterol, fiber, carbs) VALUES(:food, :servings, :id, :date, :protein, :sodium, :sugar, :fat, :calories, :cholesterol, :fiber, :carbs)",
            food = quote["food"],
            servings = servings,
            id = session["user_id"],
            date = time,
            protein = round(servings*float((quote["protein"])[:-1]), 1),
            sodium = round(servings*float((quote["sodium"])[:-2]), 1),
            sugar = round(servings*float((quote["sugars"])[:-1]),1),
            fat = round(servings*float((quote["total fat"])[:-1]), 1),
            calories = round(servings*quote["calories"], 1),
            cholesterol = round(servings*float((quote["cholesterol"])[:-2]), 1),
            fiber = round(servings*float((quote["fiber"])[:-1]), 1),
            carbs = round(servings*float((quote["carbs"])[:-1]), 1))

        else:
            serv = servings + more[0]["servings"]
            db.execute("UPDATE history SET servings = :servings, date = :date, protein = :protein, sodium = :sodium, sugar = :sugar, fat = :fat, calories = :calories, cholesterol = :cholesterol, fiber = :fiber, carbs = :carbs WHERE id = :user_id AND food = :food",
            servings = serv,
            user_id = session["user_id"],
            food = quote["food"],
            date = time,
            protein = round(serv*float((quote["protein"])[:-1]), 1),
            sodium = round(serv*float((quote["sodium"])[:-2]), 1),
            sugar = round(serv*float((quote["sugars"])[:-1]),1),
            fat = round(serv*float((quote["total fat"])[:-1]), 1),
            calories = round(serv*quote["calories"], 1),
            cholesterol = round(serv*float((quote["cholesterol"])[:-2]), 1),
            fiber = round(serv*float((quote["fiber"])[:-1]), 1),
            carbs = round(serv*float((quote["carbs"])[:-1]), 1))

        # Direct user back to meal plan
        flash("Created!")
        return redirect("/")

    else:
        # Render information into html page
        objects = printing()[0]
        things = breakfast()
        return render_template("menu.html", dictionary = objects, keys = objects.keys())


@app.route("/breakfast", methods=["GET", "POST"])
def brekkie():
    """Add food into meal plan"""

    if request.method == "POST":
        quote = lookup(request.form.get("id"))

        # Check if the food id exists
        if not quote:
            return apology("No nutrional info found", 400)

        # Check if the servings specified was a positive integer
        try:
            servings = int(request.form.get("servings"))
        except:
            return apology("servings must be a positive integer", 400)

        # Check if the number of servings requested was 0 or not
        if servings <= 0:
            return apology("cannot buy 0 or fewer servings", 400)

        # Query database for history
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.execute("INSERT INTO history (food, servings, id, date, protein, sodium, sugar, fat, calories, cholesterol, fiber, carbs) VALUES(:food, :servings, :id, :date, :protein, :sodium, :sugar, :fat, :calories, :cholesterol, :fiber, :carbs)",
        food = quote["food"],
        servings = servings,
        id = session["user_id"],
        date = time,
        protein = round(servings*float((quote["protein"])[:-1]), 1),
        sodium = round(servings*float((quote["sodium"])[:-2]), 1),
        sugar = round(servings*float((quote["sugars"])[:-1]),1),
        fat = round(servings*float((quote["total fat"])[:-1]), 1),
        calories = round(servings*quote["calories"], 1),
        cholesterol = round(servings*float((quote["cholesterol"])[:-2]), 1),
        fiber = round(servings*float((quote["fiber"])[:-1]), 1),
        carbs = round(servings*float((quote["carbs"])[:-1]), 1))

        # Direct user back to meal plan
        flash("Created!")
        return redirect("/")

    else:
        # Render information into html page
        objects = printing()[1]
        things = breakfast()
        return render_template("breakfast.html", dictionary = objects, breakfast = things)


@app.route("/lunch", methods=["GET", "POST"])
def lunchie():
    """Add food into meal plan"""

    if request.method == "POST":
        quote = lookup(request.form.get("id"))

        # Check if the food id exists
        if not quote:
            return apology("No nutrional info found", 400)

        # Check if the servings specified was a positive integer
        try:
            servings = int(request.form.get("servings"))
        except:
            return apology("servings must be a positive integer", 400)

        # Check if the number of servings requested was 0 or not
        if servings <= 0:
            return apology("cannot buy 0 or fewer servings", 400)

        # Query database for history
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.execute("INSERT INTO history (food, servings, id, date, protein, sodium, sugar, fat, calories, cholesterol, fiber, carbs) VALUES(:food, :servings, :id, :date, :protein, :sodium, :sugar, :fat, :calories, :cholesterol, :fiber, :carbs)",
        food = quote["food"],
        servings = servings,
        id = session["user_id"],
        date = time,
        protein = round(servings*float((quote["protein"])[:-1]), 1),
        sodium = round(servings*float((quote["sodium"])[:-2]), 1),
        sugar = round(servings*float((quote["sugars"])[:-1]),1),
        fat = round(servings*float((quote["total fat"])[:-1]), 1),
        calories = round(servings*quote["calories"], 1),
        cholesterol = round(servings*float((quote["cholesterol"])[:-2]), 1),
        fiber = round(servings*float((quote["fiber"])[:-1]), 1),
        carbs = round(servings*float((quote["carbs"])[:-1]), 1))

        # Direct user back to meal plan
        flash("Created!")
        return redirect("/")

    else:
        # Render information onto html page
        objects = printing()[1]
        things = lunch()
        return render_template("lunch.html", dictionary = objects, lunch = things)


@app.route("/dinner", methods=["GET", "POST"])
def dinn():
    """Add food into meal plan"""

    if request.method == "POST":
        quote = lookup(request.form.get("id"))

        # Check if the food id exists
        if not quote:
            return apology("No nutrional info found", 400)

        # Check if the servings specified was a positive integer
        try:
            servings = int(request.form.get("servings"))
        except:
            return apology("servings must be a positive integer", 400)

        # Check if the number of servings requested was 0 or not
        if servings <= 0:
            return apology("cannot buy 0 or fewer servings", 400)

        # Query database for history
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.execute("INSERT INTO history (food, servings, id, date, protein, sodium, sugar, fat, calories, cholesterol, fiber, carbs) VALUES(:food, :servings, :id, :date, :protein, :sodium, :sugar, :fat, :calories, :cholesterol, :fiber, :carbs)",
        food = quote["food"],
        servings = servings,
        id = session["user_id"],
        date = time,
        protein = round(servings*float((quote["protein"])[:-1]), 1),
        sodium = round(servings*float((quote["sodium"])[:-2]), 1),
        sugar = round(servings*float((quote["sugars"])[:-1]),1),
        fat = round(servings*float((quote["total fat"])[:-1]), 1),
        calories = round(servings*quote["calories"], 1),
        cholesterol = round(servings*float((quote["cholesterol"])[:-2]), 1),
        fiber = round(servings*float((quote["fiber"])[:-1]), 1),
        carbs = round(servings*float((quote["carbs"])[:-1]), 1))

        # Direct user back to meal plan
        flash("Created!")
        return redirect("/")

    else:
        objects = printing()[1]
        things = dinner()
        return render_template("dinner.html", dictionary = objects, dinner = things)


@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    """Remove food from meal plan"""

    foods = db.execute("SELECT food FROM history WHERE id = :user_id", user_id=session["user_id"])
    if request.method == "POST":

        # Ensure a valid food
        if not request.form.get("food"):
            return apology("no food was selected", 400)

        food = request.form.get("food")
        # Select user's servings

        db.execute("DELETE FROM history WHERE id = :user_id AND food = :food", user_id = session["user_id"], food = food)



        flash("Removed!")

        # Redirect the user to meal plan
        return redirect("/")
    else:
        return render_template("remove.html", foods = foods)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/lookup", methods=["GET", "POST"])
@login_required
def lookuping():
    """Get food nutrition information."""

    if request.method == "POST":
        quote = lookup(request.form.get("id"))
        print("quotess", quote)
        if quote == None:
            return apology("food is invalid", 400)

        return render_template("lookedup.html", quote = quote)

    # User reached route via GET (as by clicking a link or via redi)
    else:
        return render_template("lookup.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure that "Confirm password" and "Password" inputs are the same
        elif request.form.get("confirmPassword") != request.form.get("password"):
            return apology("passwords do not match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username does not exist
        if len(rows) != 0:
            return apology("username already exists", 403)

        # Insert user into database
        newUser = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"),
                            hash=generate_password_hash(request.form.get("password")))

        # Remember which user has logged in
        session["user_id"] = newUser

        flash("Registered!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)