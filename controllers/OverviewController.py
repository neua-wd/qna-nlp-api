from flask_restful import Resource, reqparse

from models.Overview import Overview


class OverviewController(Resource):
    # Returns the overview of a particular question is a question is supplied
    # Returns a random overview if no question is supplied
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('question', type=str)

            question = parser.parse_args()['question']
            if (question):
                return Overview().find(question)
            else:
                return Overview().sample()
        except Exception as e:
            return {'error': e.args}

    def patch(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('question_id', type=str)
            parser.add_argument('explanation_column', type=str)
            # Passing a list of strings with flask_restful is a known bug
            # The issue is still open
            # A workaround is to set parameters like below
            parser.add_argument('new_facts', required=True,
                                type=str, action='append', default=[],
                                help='Please provide the new_facts')

            question_id = parser.parse_args()['question_id']
            explanation_column = parser.parse_args()['explanation_column']
            new_facts = parser.parse_args()['new_facts']

            return Overview().update_explanation(question_id,
                                                 explanation_column,
                                                 new_facts)
        except Exception as e:
            return {'error': e.args}
