from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'jasonmaelrin'  # For session management

# SQLite Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model (storing user credentials)
class TravelSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Travel Info
    travel_name = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100))
    bus_type = db.Column(db.String(50))
    brand_of_bus = db.Column(db.String(100))
    register_number = db.Column(db.String(100))
    bus_timing = db.Column(db.String(100))
    total_seats = db.Column(db.Integer)
    cost_of_seat = db.Column(db.Integer)
    bus_route_start = db.Column(db.String(100))
    bus_connecting_routes = db.Column(db.String(255))
    bus_route_end = db.Column(db.String(100))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def setpassword(self,password):
        self.password_hash=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
# ---------- Auto Create Tables ----------
@app.route("/")
def create_tables():
    db.create_all()
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('index.html')


@app.route('/sign', methods=['POST'])  # 👈 This is the key part
def sign():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']


        user = User.query.filter_by(username=username).first()

        if user:
            return render_template("login.html", error="User Already Exists")
        else:
            new_user = User(username=username, role=role)
            new_user.setpassword(password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('booking'))
    
    return render_template("sign.html")

@app.route("/login-r")
def relogin():
    return render_template("login.html")



@app.route("/login", methods=['POST'])
def login():
    
    username = request.form['username']
    password = request.form['password']
    role= request.form['role']

# Query the database to find the user by username and password
    user = User.query.filter_by(username=username, password=password,role=role).first()

    if user and User.check_password(password):
        session['username'] = username
        return render_template("booking_page.html")  # Store username in session
        
    else:
        print( "Invalid credentials. Please try again.")
        return render_template('index.html')


@app.route('/booking')
def booking_page():
    return render_template('booking_page.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('/'))


if __name__ == '__main__':
    app.run(debug=True)
