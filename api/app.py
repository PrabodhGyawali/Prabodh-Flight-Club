import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from database import db

load_dotenv(dotenv_path='.flaskenv')

# Create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_URI')
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/users/create", methods=["GET", "POST"])
def create():
    # do backend checks
    # add user to DB
    # if (error) {Post to front end} 
    return "log user added"

if __name__ == "__main__":
    app.run(debug=True)