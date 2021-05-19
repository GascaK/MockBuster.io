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

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)