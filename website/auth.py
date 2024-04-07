from flask import Blueprint, render_template, request, redirect, url_for, flash
from re import match
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth=Blueprint('auth', __name__)

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        password2=request.form.get('password2')


        #if email already exists, i.e. Only one user_name/account issued per email address
        email_exists= User.query.filter_by(email= email).first()
        username_exists= User.query.filter_by(username=username).first()        
        #Check if email is valid using [regex]
        email_valid=True    
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'        
        if not match(pattern, email):
            email_valid=False


        if email_exists:
            flash(f"Another account already associated with this email: {email}", category='error')
        elif username_exists:
            flash(f"Another account already associated with this username: {username}", category='error')
        elif password!=password2:
            flash("Password do not match. Try again.", category='error')        
        elif len(password)>8:
            flash("password length exceeds 8 characters.", category='error')
        elif len(password)<6:
            flash("password length can't be less than 6 characters.", category='error')
        elif not email_valid:
            flash(f"Email is not valid, check the format: {email}")                                                                                                                                                
        else:
            #HASH THE PASSWORD MOTHERFCUKER
            password_hash= generate_password_hash(password, method='scrypt')    #method='sha256'                        

            new_user=User(email=email, username=username, password=password_hash)       
            db.session.add(new_user)
            db.session.commit()            

            # After sign-up, sign-in the user straightaway                        
            login_user(new_user, remember=True)
            flash("Congratulations, Welcome to Blog_Burg!")

            return redirect(url_for('views.home'))    
    
    return render_template("signup.html", user=current_user)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')                
        password=request.form.get('password')            

        user_exists= User.query.filter_by(username=username).first() 
        # if doesn't exists return NULL, otherwise returns user object    
        if user_exists:
            if check_password_hash(user_exists.password, password):
                flash("User successfuly logged in! Redirecting...", category='success')                
                login_user(user_exists, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Password entered is incorrect. Try again.", category='error') 
        else:
            flash(f"user [{username}] doesn't exist. Please check the username you entered.", category='error')

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()    
    return redirect(url_for('views.home'))








