from flask_restful import Resource
from mbuster import api, db

class MbusterMovies(Resource):
    def get(self, user_id):
        return {user_id: user_id}

    def delete(self, user_id):
        return {"Deleted": user_id}

api.add_resource(MbusterMovies, "/movies_api/<user_id>")