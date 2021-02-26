from flask_restful import Resource, reqparse

from models.Overview import Overview


class OverviewController(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('question', type=str, required=True,
                help='Please provide the question')

            return Overview().find(parser.parse_args()['question'])
        except Exception as e:
            return { 'error': e.args }