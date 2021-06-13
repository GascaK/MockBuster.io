from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mbuster import app, db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(20),  unique=True, nullable=False)
    password   = db.Column(db.String(60),  nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)

    # Movie Relationship.
    movies = db.relationship("Movies", backref="owner", lazy=True)

    def get_reset_token(self, expires=1800):
        s = Serializer(app.config['SECRET_KEY'], expires)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    m_title = db.Column(db.String(30), nullable=False, default="")
    m_count = db.Column(db.Integer, default=1)
    m_stock = db.Column(db.Boolean, nullable=False, default=True)
    imdb_id = db.Column(db.String(20), default="")

    def __repr__(self):
        return f"Movie('{self.m_title}', '{self.m_stock}')"