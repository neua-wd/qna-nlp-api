from flask_restful import Resource, reqparse

from models.Overview import Overview


class OverviewController(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('question', type=str,
                                help='Please provide the question')

            question = parser.parse_args()['question']
            if (question):
                return Overview().find(question)
            else:
                return Overview().sample()

        except Exception as e:
            print(e)
            return {'error': e.args}
