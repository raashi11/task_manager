from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import logging


app = Flask(__name__)
app.config["SECRET_KEY"] = "some_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
SECRET_KEY = "some_secret_key"

db = SQLAlchemy(app)
logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


@app.route("/")
def home():
    if "token" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        user = User.query.filter_by(username=data["username"]).first()
        if user and check_password_hash(user.password, data["password"]):
            token = jwt.encode(
                {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=1)},
                SECRET_KEY,
                algorithm="HS256",
            )
            session["token"] = token
            logging.info(f"User {user.username} logged in successfully.")
            return redirect(url_for("dashboard"))
        logging.warning("Invalid login attempt.")
        return "Invalid credentials", 401

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        existing_user = User.query.filter_by(username=data["username"]).first()

        if existing_user:
            logging.warning(f"Registration attempt with existing username: {data['username']}")
            return "Username already exists. Please choose a different username", 400

        hashed_password = generate_password_hash(
            data["password"], method="pbkdf2:sha256", salt_length=8
        )
        new_user = User(username=data["username"], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        logging.info(f"User {new_user.username} registered successfully.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "token" not in session:
        return redirect(url_for("login"))

    try:
        token = session["token"]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        tasks = Task.query.filter_by(user_id=decoded["user_id"]).all()
        return render_template("dashboard.html", tasks=tasks)
    except jwt.ExpiredSignatureError:
        logging.error("JWT token has expired.")
        return redirect(url_for("login"))
    except jwt.InvalidTokenError:
        logging.error("Invalid JWT token.")
        return redirect(url_for("login"))


@app.route("/add-task", methods=["POST"])
def add_task():
    if "token" not in session:
        return redirect(url_for("login"))

    try:
        token = session["token"]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        data = request.form
        new_task = Task(
            title=data["title"],
            description=data["description"],
            user_id=decoded["user_id"],
        )
        db.session.add(new_task)
        db.session.commit()
        logging.info("Task added successfully.")
        return redirect(url_for("dashboard"))
    except jwt.InvalidTokenError:
        logging.error("Invalid JWT token.")
        return redirect(url_for("login"))


@app.route("/delete-task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "token" not in session:
        return redirect(url_for("login"))

    try:
        token = session["token"]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        task = Task.query.filter_by(id=task_id, user_id=decoded["user_id"]).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            logging.info(f"Task {task_id} deleted successfully.")
        return redirect(url_for("dashboard"))
    except jwt.InvalidTokenError:
        logging.error("Invalid JWT token.")
        return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=True)
