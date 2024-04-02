from flask_app import app, bcrypt
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User


@app.route("/")
def index():
    """This route displays the login and reg form"""
    return render_template("index.html")


@app.post("/users/register")
def register():
    """This route proccesses the reqgister form."""
    print("\n\n\nform:", request.form)
    # If form not vaild redirect
    if not User.validate_register(request.form):
        print("\n\n\nvalidation failed")
        return redirect("/")

    print("\n\n\nvalidation passed")
    # check if user already exists
    potential_user = User.find_by_email(request.form["email"])

    # If user exists redirect
    if potential_user != None:
        flash("Email in user, Please log in!", "register")
        return redirect("/")

    # user does not exists, safe to create and hash a password
    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
    }
    user_id = User.register(user_data)
    # save user id in session (log them in)
    session["user_id"] = user_id
    return redirect("/users/dashboard")


@app.post("/users/login")
def login():
    """This route proccesses the login form."""

    # If form not vaild redirect
    if not User.validate_login(request.form):
        return redirect("/")

    # does user exists?
    potential_user = User.find_by_email(request.form["email"])
    # user does not exists redirect
    if potential_user == None:
        flash("Invalid credentials.")
        return redirect("/")

    # user exists!
    user = potential_user

    # check the passowrd
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials", "login")
        return redirect("/")

    # save user id in session (log them in)
    session["user_id"] = user.id
    return redirect("/users/dashboard")


@app.get("/users/logout")
def logout():
    """This route clears session."""
    session.clear()
    return redirect("/")


@app.get("/users/dashboard")
def dashboard():
    """This route display the user dasshboard"""
    if "user_id" not in session:
        flash("You must be logged in to view that page.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])
    return render_template("all_records.html", user=user)
