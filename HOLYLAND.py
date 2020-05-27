from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/holyland'
db = SQLAlchemy(app)



# config or connecting to MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '1234567890'
app.config['MYSQL_DB'] = 'holyland'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


#init or initialize MySQL
mysql = MySQL(app)


#Posts = Posts()






@app.route('/')
def home():
    return render_template('home.html')


@app.route('/holyland_tour')
def holyland_tour():
    return render_template('holyland_tour.html')


@app.route('/jud_chris')
def jud_chris():
    return render_template('jud_chris.html')


@app.route('/jud_chris_vid')
def jud_chris_vid():
    return render_template('jud_chris_vid.html')


@app.route('/about_israel')
def about_israel():
    return render_template('about_israel.html')


@app.route('/songs')
def songs():
    return render_template('songs.html')






# Signup Form Class
class SignupForm(Form):

    name = StringField('Name', [validators.Length(min=1, max=50)],)
    username = StringField('Username', [validators.Length(min=3, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')





# User register or signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():

        # now getting the form values
        name = form.name.data   # getting the form value name
        email = form.email.data  # getting email
        username = form.username.data # getting username
        password = sha256_crypt.encrypt(str(form.password.data))

        # create cursor
        cur = mysql.connection.cursor()

        #execute query
        cur.execute("INSERT INTO signup_form(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # commit to DB
        mysql.connection.commit()

        # close connection
        cur.close()

        flash('You are registered, you can do login now', 'success')

        return redirect(url_for('signin'))

    return render_template('signup.html', form=form)









# User login or signin
@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # create cursor
        cur = mysql.connection.cursor()

        # Get signup_form by username
        result = cur.execute("SELECT * FROM signup_form WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in, you can now complete your holyland tour registration and access holyland blog', 'success')
                return redirect(url_for('holyland_blog'))
            else:
                error = 'Invalid login'
                return render_template('signin.html', error=error)

            # Close connection
            cur.close()

        else:
            error = 'Username not found'
            return render_template('signin.html', error=error)

    return render_template('signin.html')





# Check if user logged in
def is_logged_in(f):
    @wraps(f)          # and for this code you have to import from functools import wraps
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('unauthorized, please login first', 'danger')
            return redirect(url_for('signin'))
    return wrap





#Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('signin'))







# making of registration form class.    # for registration, we have used sqlalchemy, not mysqldb
class Registration_form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    mob_no = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    alter_mob_no = db.Column(db.String(50), nullable=False)
    alter_email = db.Column(db.String(50), nullable=False)
    tour_season = db.Column(db.String(50), nullable=False)
    house_no = db.Column(db.String(50), nullable=False)
    home_area = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    church_name = db.Column(db.String(50), nullable=False)
    qualification = db.Column(db.String(50), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    disability = db.Column(db.String(50), nullable=False)
    tour_earlier = db.Column(db.String(50), nullable=False)
    food = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(50), nullable=False)


@app.route("/registration_form", methods=['GET', 'POST'])
@is_logged_in
def registration():
    if (request.method == 'POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        mob_no = request.form.get('mob_no')
        email = request.form.get('email')
        alter_mob_no = request.form.get('alter_mob_no')
        alter_email = request.form.get('alter_email')
        tour_season = request.form.get('tour_season')
        house_no = request.form.get('house_no')
        home_area = request.form.get('home_area')
        city = request.form.get('city')
        country = request.form.get('country')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        church_name = request.form.get('church_name')
        qualification = request.form.get('qualification')
        profession = request.form.get('profession')
        disability = request.form.get('disability')
        tour_earlier = request.form.get('tour_earlier')
        food = request.form.get('food')
        age = request.form.get('age')

        registration = Registration_form(name=name, username=username, mob_no=mob_no, email=email, alter_mob_no=alter_mob_no, alter_email=alter_email, tour_season=tour_season, house_no=house_no, home_area=home_area, city=city, country=country, state=state, zip_code=zip_code, church_name=church_name, qualification=qualification, profession=profession, disability=disability, tour_earlier=tour_earlier, food=food, age=age)
        db.session.add(registration)
        db.session.commit()

        flash('Thanks for your registration, we acknowledge you once we schedule the tour', 'success')
        # return redirect(url_for('holyland_tour'))
    return render_template('registration_form.html')




'''
@app.route('/registration_form', methods=['GET', 'POST'])
@is_logged_in
def registration_form():

    if request.method == 'POST':
        # Get Form Fields
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        #password_candidate = request.form['password']


        # create cursor
        cur = mysql.connection.cursor()

        # Get signup_form by username
        result = cur.execute("SELECT * FROM signup_form WHERE username = %s AND name = %s AND email = %s", [username], ['name'], ['email'] )

        if session['logged_in'] and session['name'] and session['email'] and session['username']:
            pass
        else:
            error = 'Invalid username, name or email'
            return render_template('registration_form.html', error=error)

        # Close connection
        cur.close()



    else:
        error = 'Username not found'
        return render_template('registration_form.html', error=error)

    return render_template('registration_form.html')
    '''





# making of enquiry class.  # for enquery, we have used sqlalchemy
class Enquiry_form(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_no = db.Column(db.String(50), nullable=False)
    msg = db.Column(db.String(300), nullable=False)
    #date = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable=False)


@app.route("/enquiry", methods=['GET', 'POST'])
def enquiry():
    if(request.method=='POST'):

        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Enquiry_form(name=name, phone_no=phone, msg=message, email=email)
        db.session.add(entry)
        db.session.commit()
        flash('Thanks for your query, we will respond as soon as possible', 'success')
        #return redirect(url_for('holyland_tour'))
    return render_template('enquiry.html')





@app.route('/holyland_blog')
@is_logged_in
def holyland_blog():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get Posts
    result = cur.execute("SELECT * FROM holyland_blog_post")

    posts = cur.fetchall()

    if result > 0:
        return render_template('holyland_blog.html', posts=posts)
    else:
        msg = 'No Posts found'
        return render_template('holyland_blog.html', msg=msg)

    # Close connection
    cur.close()

    return render_template('holyland_blog.html')



# Post Form Class
class PostForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)],)
    body = TextAreaField('Body', [validators.Length(min=30)])




# Add Posts
@app.route('/add_post', methods=['GET', 'POST'])
@is_logged_in
def add_post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO holyland_blog_post(title, body, author) VALUES(%s, %s, %s)", (title, body, session['username']))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Post Created', 'success')

        return redirect(url_for('holyland_blog'))

    return render_template('add_post.html', form=form)






# Edit Posts
@app.route('/edit_post/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_post(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get post by id
    result = cur.execute("SELECT * FROM holyland_blog_post WHERE id = %s", [id])
    post = cur.fetchone()

    # Get form
    form = PostForm(request.form)

    # Populate post from fields
    form.title.data = post['title']
    form.body.data = post['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("UPDATE holyland_blog_post SET title=%s, body=%s WHERE id=%s",(title, body, id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Post updated', 'success')

        return redirect(url_for('holyland_blog'))

    return render_template('edit_post.html', form=form)





# Delete Post
@app.route('/delete_post/<string:id>', methods=['POST'])
@is_logged_in
def delete_post(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM holyland_blog_post WHERE id = %s", [id])
    # !Rjfmpet&n!wrmpf
    # Commit to DB
    mysql.connection.commit()

    # Close connection
    cur.close()
    flash('Post deleted', 'success')

    return redirect(url_for('holyland_blog'))






if __name__ == '__main__':
    app.secret_key = 'secret037'
    app.run(host='127.0.0.1', port='5000',debug=True)

# template or view, both are same meaning