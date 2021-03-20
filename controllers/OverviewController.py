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
            print(e)
            return {'error': e.args}

    # Remove a fact from an explanation
    def patch(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('question_id', type=str)
            parser.add_argument('explanation_column', type=str)
            parser.add_argument('fact_id', type=str)
            # Passing a list of strings with flask_restful is a known bug
            # The issue is still open
            # A workaround is to set parameters like below
            parser.add_argument('new_order', required=False,
                                type=str, action='append', default=[])

            question_id = parser.parse_args()['question_id']
            explanation_column = parser.parse_args()['explanation_column']
            fact_id = parser.parse_args()['fact_id']
            new_oder = parser.parse_args()['new_order']

            if (not (fact_id or new_oder)):
                return {'error': 'Please provide either the new_order or the fact_id'}

            if (fact_id):
                return Overview().remove_fact(question_id, explanation_column,
                                              fact_id)
            else:
                return Overview().update_explanation_order(question_id,
                                                           explanation_column,
                                                           new_oder)
        except Exception as e:
            return {'error': e.args}
