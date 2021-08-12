from flask_restful import Resource, reqparse
from flask import jsonify
from mbuster.models import User, Movies
from mbuster import api, db, ia


class UserMovies(Resource):
    def __init__(self):
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("key", help="API 'key' is Required", required=True)
        self.post_args = reqparse.RequestParser()
        self.post_args.add_argument("count")
        self.post_args.add_argument("stock")
        self.post_args.add_argument("key", help="API 'key' is Required", required=True)
        self.post_args.add_argument("imdb", help="'imdb' ID is required.", required=True)
        super(UserMovies, self).__init__()

    def post(self, username):
        # Parse arguments.
        args = self.post_args.parse_args()
        # Query db.
        query = db.session.query(User, Movies).\
            join(Movies).\
            filter(User.username==username, User.API_KEY==args["key"]).all()

        for user, movies in query:
            temp = user.id
            if movies.imdb_id == args["imdb"]:
                return ({409: f"ID {args['imdb']} already exists for user."})

        # IDMB API get. IMDB Prepends 2 values.
        search = ia.get_movie(args.imdb[1:])
        # Create new movie object.
        movie  = Movies(user_id=temp,
                        m_title=search["title"],
                        m_count=args["count"] or 1,
                        m_stock=args["stock"] or True,
                        imdb_id=search['imdbID'])
        db.session.add(movie)
        db.session.commit()
        return ({201: "A new resource was successfully created."})

    def get(self, username):
        # Parse arguments.
        args = self.get_args.parse_args()
        # Query DB.
        query = db.session.query(User, Movies).\
            join(Movies).\
            filter(User.username==username, User.API_KEY==args["key"]).all()

        # Query object is empty.
        if not query:
            return ({409: "That combination user and API does not exist."})

        temp = {username: []}
        for user, movies in query:
            temp[username].append({
                "Title" : movies.m_title,
                "Inventory" : movies.m_count,
                "In stock?" : movies.m_stock,
                "IMDB ID" : movies.imdb_id
            })
        return jsonify(temp)

    def put(self):
        return ({405: "Resource not supported."})

    def delete(self, user_id):
        return ({405: "Resource not supported."})

class UserProfile(Resource):
    def __init__(self):
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("key", help="API key required.", required=True)

    def post(self):
        return ({405: "Resource not supported."})

    def get(self, username):
        args = self.get_args.parse_args()
        query = db.session.query(User).\
            filter(User.username==username, User.API_KEY==args["key"]).first()

        if not query:
            return ({409: "That combination user and API does not exist."})

        temp = {username: []}
        temp[username] = ({
            "ID" : query.id,
            "Email": query.email,
            "API Key" : query.API_KEY
        })

        return jsonify(temp)

    def put(self):
        pass

    def delete(self):
        pass

api.add_resource(UserProfile, "/api/<username>")
api.add_resource(UserMovies, "/api/<username>/movies")