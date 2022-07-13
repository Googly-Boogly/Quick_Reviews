from datetime import datetime
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.review import Review
from flask_app.templates import app
from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash

@app.route("/")
def register():
    session['user_id'] = 0
    return render_template("loginpage.html")

@app.route("/discover")
def discover():
    rests = Review.get_random_6_reviews()
    for x in rests:
        print(x['rest_name'])
        print(x['id'])
    # print(rests)
    rests1 = [rests[0], rests[1]]
    rests2 = [rests[2], rests[3]]
    rests3 = [rests[4], rests[5]]
    return render_template("discover.html", first_name=session['name'], restaurants1=rests1, restaurants2=rests2, restaurants3=rests3, user_id=session['user_id'])

@app.route("/home")
def home():
    data = {
        'user_id': session['user_id']
    }
    temp = Review.get_all_user(data)
    if len(temp) > 9:
        rests = temp[0:10]
    elif len(temp) < 9:
        rests = temp[0:len(temp)]
    return render_template("homepage.html", reviews=rests, user_id=session['user_id'])

@app.route("/popular")
def popular():
    temp = Review.get_popular_page()
    return render_template("popular.html", first_name=session['name'], reviews=temp, user_id=session['user_id'])

@app.route("/profile")
def profile():
    return render_template("profile.html", fname=session['name'], user_id=session['user_id'])

@app.route("/review")
def review_page():
    return render_template("review.html", first_name=session['name'], user_id=session['user_id'])



@app.route("/change/password", methods=['POST'])
def registgdfgerfg():
    if request.form['new_pass'] != request.form['conf_new_pass']:
        flash("New passwords not the same")
        return redirect("/profile")
    data = { "id" : session['user_id'] }
    user_in_db = User.get_by_id(data)
    # user is not registered in the db
    print(user_in_db)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/profile")
    print(request.form)
    x = request.form['password']
    print(x)
    y = user_in_db[0]['password']
    if not check_password_hash(y, x):
        # if we get False after checking the password
        flash("Enter the correct password")
        return redirect('/profile')
    password_hash = generate_password_hash(request.form['new_pass'])
    User.update_one_password({'new_pass': password_hash, 'id':session['user_id']})
    # if the passwords matched, we set the user_id into session
    return redirect("/home")



@app.route("/logout", methods=['POST'])
def logout():
    session['user_id'] = ''
    session['name'] = ''
    return redirect('/')

@app.route("/register", methods=['POST'])
def register_post():
    if not User.validate_creds(request.form):
        return redirect('/')
    password_hash = generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': password_hash,
    }
    User.save(data)
    return redirect('/')

@app.route("/login", methods=['POST'])
def loggin():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['name'] = user_in_db.fname
    return redirect("/home")

@app.route("/add_review", methods=['POST'])
def add_review():
    now = datetime.now()
    data = {
        'rating': request.form.get('rating'),
        'review': request.form['review'],
        'added': str(now),
        'updated': str(now),
        'user_id': session['user_id'],
        'rest_name': request.form['Restuarant_Name'],
        }
    Review.save(data)
    return redirect("/home")





