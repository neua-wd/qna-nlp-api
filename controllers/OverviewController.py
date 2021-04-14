from flask_restful import Resource, reqparse

from models.Overview import Overview
from models.Question import Question


class OverviewController(Resource):
    # Returns the overview of a particular question is a question is supplied
    # Returns a random overview if no question is supplied
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('question', type=str)

            question = parser.parse_args()['question']
            if (question):
                row = Question().get_row_by_question(question)
            else:
                row = Question().sample()

            return Overview().get_overview_from_row(row)
        except Exception as e:
            return {'error': e.args}

    # Update the fact IDs in a question row
    # Used for updating the ordering and for removing facts
    def patch(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('update_type', type=str, required=True,
                                help='Please provide the update type')

            parser.add_argument('question_id', type=str)
            parser.add_argument('explanation_column', type=str)
            # Passing a list of strings with flask_restful is a known bug
            # The issue is still open
            # A workaround is to set parameters like below
            parser.add_argument('new_facts', type=str,
                                action='append', default=[])

            parser.add_argument('new_answer', type=str)

            parser.add_argument('new_fact_id', type=str)

            update_type = parser.parse_args()['update_type']

            args = parser.parse_args()

            if (update_type == 'facts'):
                self.__update_explanation(args['question_id'],
                                          args['explanation_column'],
                                          args['new_facts'])
            elif (update_type == 'answer'):
                self.__update_answer(args['question_id'], args['new_answer'])
            elif (update_type == 'add fact'):
                self.__add_fact(args['question_id'],
                                args['explanation_column'],
                                args['new_fact_id'])
            else:
                return {'error': 'update_type can only be "facts", "answers" or "add fact'}, 422

            updated_row = Question().get_row_by_id(args['question_id'])

            return Overview().get_overview_from_row(updated_row)
        except Exception as e:
            return {'error': e.args}

    def __update_explanation(self, question_id, explanation_column, new_facts):
        Question().update_explanation(question_id,
                                      explanation_column,
                                      new_facts)

    def __update_answer(self, question_id, new_answer):
        Question().change_answer(question_id, new_answer)

    def __add_fact(self, question_id, explanation_column, new_fact_id):
        Question().add_fact_to_explanation(question_id,
                                           explanation_column,
                                           new_fact_id)
