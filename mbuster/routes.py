from mbuster.forms import RegistrationForm
from flask import Flask, url_for, render_template, flash, redirect
from mbuster.forms import RegistrationForm, LoginForm
from mbuster import app

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created! Congrats {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template("login.html", title="Login", form=form)

@app.route("/about")
def about_us():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("about.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")