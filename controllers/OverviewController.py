from flask_restful import Resource, reqparse

from models.Overview import Overview


class OverviewController(Resource):
    # Returns the overview of a particular question is a question is supplied
    # Returns a random overview if no question is supplied
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

    # Remove a fact from an explanation
    def patch(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('question_id', type=str,
                                help='Please provide the question ID')
            parser.add_argument('fact_id', type=str,
                                help='Please provide the fact ID')
            parser.add_argument('explanation', type=str,
                                help='Please specify the choice (eg. explanationA)')

            question_id = parser.parse_args()['question_id']
            fact_id = parser.parse_args()['fact_id']
            explanation = parser.parse_args()['explanation']

            return Overview().remove_fact(question_id, fact_id, explanation)
        except Exception as e:
            return {'error': e.args}
