from mbuster.forms import RegistrationForm
from flask import Flask, url_for, render_template, flash, redirect
from mbuster.forms import RegistrationForm, LoginForm, AddMovieForm
from mbuster import app, db, bcrypt
from mbuster.models import User, Movies
from flask_login import login_user, logout_user, current_user

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! Congrats {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    form = AddMovieForm()
    ask = Movies.query.filter_by(user_id=current_user.id)
    movies = ask.all()
    if form.validate_on_submit():
        if ask.filter_by(m_title=form.movie_title.data).first():
            flash('Movie already in list.', 'warning')
        else:
            nMovie = Movies(user_id=current_user.id,
                            m_title=form.movie_title.data,
                            m_stock=(False if form.stock.data else True), # Uno Reverse
                            m_count=1)
            db.session.add(nMovie)
            db.session.commit()
            flash(f'{form.movie_title.data} added!', 'success')

    return render_template("dashboard.html", title="", form=form, movies=movies)

@app.route("/about")
def about_us():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")