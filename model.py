from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from hybridbot import app
from datetime import datetime

# creates sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True)
    welcomed_at = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.date)
    message_counts = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"User: {self.name}, {self.email}"


class WelcomeMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    text = db.Column(db.Text, nullable=False)
    channel_id = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Message: {self.title}, {self.text}"


#db.drop_all()  # to reset
db.create_all()
# db.query_all() to view db
