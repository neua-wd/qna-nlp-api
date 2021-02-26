from flask_restful import Resource, reqparse

from models.Fact import Fact
from models.Overview import Overview


class FactController(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('table_name', type=str, required=True, 
                help='Please provide the table name')
            parser.add_argument('to_question', type=str, required=True,
                help='Please provide the question ID')
            parser.add_argument('new_fact', type=dict, required=True,
                help='Please provide the new fact')

            args = parser.parse_args()

            Fact().add(args['table_name'], args['to_question'],
                args['new_fact'])

            return Overview().find_by_id(args['to_question'])
        except Exception as e:
            return { 'error': e.args }
       

    
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('edited_fact', type=dict, required=True,
                help='Please provide the edited fact')
            
            Fact().update(parser.parse_args()['edited_fact'])

            return { 'success': True }
        except Exception as e:
            return { 'error': e.args }