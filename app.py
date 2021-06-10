from mbuster import app, db
from sqlalchemy_utils import database_exists

if __name__ == "__main__":
    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        db.create_all()
    # port=5000 is necessary on AWS.
    app.run(host='0.0.0.0', port=5000)