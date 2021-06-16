import email
from flask_login.utils import login_required
from sqlalchemy.sql.elements import Null
from mbuster.forms import RegistrationForm
from flask import Flask, url_for, render_template, flash, redirect, jsonify, request
from mbuster.forms import (RegistrationForm, LoginForm, AddMovieForm, UserMovieForm,
                            ContactForm, RequestResetForm, ResetPasswordForm)
from mbuster import app, db, bcrypt, ia, mail
from mbuster.models import User, Movies
from flask_login import login_user, logout_user, current_user
from flask_mail import Message

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    # Check if logged in.
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Form submitted.
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash password.
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # User DB object.
        user = User(username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! Congrats {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))

    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Check if logged in.
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    # Form submitted.
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # User is not empty and hashed pw is valid.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    # Flask logout
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    # Check if logged in.
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    form = AddMovieForm()
    movie_form = UserMovieForm()

    # Query Movies DB and get movie data.
    movies = Movies.query.filter_by(user_id=current_user.id).order_by(Movies.m_title).all()

    return render_template("dashboard.html", 
                            title=f"{current_user.username}",
                            movie_form=movie_form,
                            form=form,
                            movies=movies)

# Delete movie form database url. Takes 1 movie_id parameter.
@app.route("/deletemovie-<int:movie_id>", methods=["POST"])
@login_required
def delete_movie(movie_id):
    # Checks user is logged and authenticated.
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Query Database for movie_id
    deleted = Movies.query.get_or_404(movie_id)
    if deleted is not None:
        db.session.delete(deleted)
        db.session.commit()
        flash(f"Deleted movie {movie_id}", "success")
    else:
        flash(f"Movie not in Database. {movie_id}. Refresh Page", "warning")

    return redirect(url_for("dashboard"))

@app.route("/addmovie/<imdbID>", methods=["POST", "GET"])
@login_required
def add_movie(imdbID):
    # Find User Movies
    ask = Movies.query.filter_by(user_id=current_user.id)

    # Check if Movie in Movies
    if ask.filter_by(imdb_id=imdbID[2:]).first():
        flash('Movie already in list.', 'warning')
    else:
        # API is slow. Refactor here.
        search = ia.get_movie(imdbID[2:]) # API prepends TT
        nMovie = Movies(user_id= current_user.id,
                        m_title= search['title'],
                        m_stock= True,
                        m_count=1,
                        imdb_id=search['imdbID']
                        )
        db.session.add(nMovie)
        db.session.commit()
        flash(f'{search} added!', 'success')
        return redirect(url_for("dashboard"))

    return redirect(url_for("dashboard"))

@app.route("/about")
def about_us():
    return render_template("about.html", title="AboutME")

@app.route("/contact")
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        pass

    return render_template("contact.html", title="Contact", form=form)

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/reset-password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            send_reset_email(user)
        flash("If email is located, reset message will be sent.", "success")
        return redirect(url_for("login"))
    
    return render_template('reset_request.html', title='Reset', form=form)

@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_pw
        db.session.commit()
        flash(f'Your password has been updated and hashed.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html', title='Reset', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset - MockBuster",
                  sender="userhelp@mockbuster.io",
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{ url_for('reset_token', token=token, _external=True) }

If you did not make this request simply ignore this email.
    '''
    mail.send(msg)