from flask_app import app
from flask_app.models.record import Record
from flask import flash, render_template, redirect, request, session
from flask_app.models.user import User

@app.get("/records/all")
def new_recipe():
    """This route renders all the records."""
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    records = Record.find_all()
    user = User.find_by_id(session["user_id"])
    return render_template("dashboard.html", records=records, user=user)
