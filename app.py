import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


current_dir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(current_dir, 'instance')

app = Flask(__name__)
# api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(db_dir, 'moviedb.sqlite3')
db = SQLAlchemy()

app.app_context().push()

db.init_app(app)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Venue(db.Model):
    __tablename__ = 'venue'
    venue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_name = db.Column(db.String(80), nullable=False)
    place = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Venue %r>' % self.venue_name


class Show(db.Model):
    __tablename__ = 'show'
    show_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('show', lazy=True))

    def __repr__(self):
        return '<Show %r>' % self.show_name


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login.html"))
    return render_template("register.html")


@app.route("/login", methods=[ "POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    pass


@app.route("/admin/dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    pass


# @app.route("/admin")
# # @login_required
# def admin():
#     id = current_user.id
#     if id==1:
#         return render_template("admin.html")
#     else:
#         flash("You must be admin to access admin page...")
#         return url_for('dashboard')
    
# if current_user.id ==1 :
#     pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
