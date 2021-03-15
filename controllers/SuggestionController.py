from flask_restful import Resource

from models.Fact import Fact


class SuggestionController(Resource):
    def get(self):
        return Fact().get_similar()
