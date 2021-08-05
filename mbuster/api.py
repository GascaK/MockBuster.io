from flask_restful import Resource, reqparse
from flask import jsonify
from mbuster.models import User, Movies
from mbuster import bcrypt, api, db

class MbusterMovies(Resource):
    def __init__(self):
        self.api_args = reqparse.RequestParser()
        self.api_args.add_argument("key", help="API Key Required", required=True)
        super(MbusterMovies, self).__init__()

    def get(self, username):
        args = self.api_args.parse_args()
        query = db.session.query(User, Movies).filter_by(username=username, API_KEY=args["key"]).join(User).all()
        if not query:
            return ({409: "That combination user and API does not exist."})

        user = {}
        for each in query.movies.all():
            user[username] = {
                "Title" : each.m_title
            }
        return jsonify(user)

    def delete(self, user_id):
        return {"Deleted": user_id}

api.add_resource(MbusterMovies, "/api/<username>/")