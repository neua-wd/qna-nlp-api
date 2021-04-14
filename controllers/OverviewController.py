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

            parser.add_argument('new_fact', type=str)

            update_type = parser.parse_args()['update_type']

            if (update_type == 'facts'):
                return self.__updated_explanation(parser)
            elif (update_type == 'answer'):
                return self.__updated_answer(parser)
            elif (update_type == 'add fact'):
                return self.__add_fact(parser)
            else:
                return {'error': 'update_type can only be "facts", "answers" or "add fact'}, 422
        except Exception as e:
            return {'error': e.args}

    def __updated_explanation(self, parser):
        return Overview().update_explanation(parser.parse_args()['question_id'],
                                             parser.parse_args()[
            'explanation_column'],
            parser.parse_args()['new_facts'])

    def __updated_answer(self, parser):
        return Overview().update_answer(parser.parse_args()['question_id'],
                                        parser.parse_args()['new_answer'])

    def __add_fact(self, parser):
        return Overview().add_fact(parser.parse_args()['question_id'],
                                   parser.parse_args()['explanation_column'],
                                   parser.parse_args()['new_fact'])
