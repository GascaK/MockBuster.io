import email
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
    movie_form = UserMovieForm()

    # Query Movies DB and get movie data.
    ask = Movies.query.filter_by(user_id=current_user.id)
    movies = ask.all()

    if form.validate_on_submit():
        if ask.filter_by(m_title=form.movie_title.data).first():
            flash('Movie already in list.', 'warning')
        else:
            search = ia.search_movie(form.movie_title.data)[0]
            nMovie = Movies(user_id= current_user.id,
                            m_title= form.movie_title.data,
                            m_stock= not form.stock.data, # Uno Reverse
                            m_count=1,
                            idmb_id=search)
            db.session.add(nMovie)
            db.session.commit()
            flash(f'{form.movie_title.data} added!', 'success')
            return redirect(url_for("dashboard"))

    return render_template("dashboard.html", 
                            title=f"{current_user.username}",
                            movie_form=movie_form,
                            form=form,
                            movies=movies)

# Delete movie form database url. Takes 1 movie_id parameter.
@app.route("/deletemovie-<int:movie_id>", methods=["POST"])
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