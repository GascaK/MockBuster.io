from mbuster import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(20),  unique=True, nullable=False)
    password   = db.Column(db.String(60),  nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    user_image = db.Column(db.String(20),  nullable=False, default="d_image.jpg")

    # Movie Relationship.
    movies = db.relationship("Movies", backref="owner", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_image}')"

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    m_title = db.Column(db.String(30), unique=True, nullable=False)
    m_stock = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"Movie('{self.m_title}', '{self.m_stock}')"