from flask import render_template, redirect, request, session, flash

from flask_app.models.provider import Provider
from flask_app.models.patient import Patient



from flask_app import app

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    if not Provider.validate_provider(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }

    provider_id = Provider.save(data)

    session["provider_id"] = provider_id

    flash("Registration successful!", "success")

    # Provider.save(request.form)
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    # if not Provider.validate_provider(request.form):
    #     return redirect("/")
    login_data = {"email": request.form["email"]}
    provider_in_db = Provider.get_by_email(login_data)

    if not provider_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(provider_in_db.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect("/")

    session["provider_id"] = provider_in_db.id
    session["first_name"] = provider_in_db.first_name
    session["last_name"] = provider_in_db.last_name

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")