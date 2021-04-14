from flask_restful import Resource, reqparse
from gensim.models.doc2vec import Doc2Vec
import pandas as pd

from models.Fact import Fact


class SuggestionController(Resource):
    def __init__(self, suggestion_model, fact_ids):
        self.suggestion_model = suggestion_model
        self.fact_ids = fact_ids

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sentence', type=str, required=True,
                            help='Please provide the sentence')

        return Fact(self.suggestion_model,
                    self.fact_ids).get_similar(
                        parser.parse_args()['sentence'])
