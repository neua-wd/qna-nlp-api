from flask_restful import Resource, reqparse
import glob
import pandas as pd
from constants import TABLES_DIRECTORY

class Fact(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('fact_id', type=str, required=True, help='Please provide the fact id')
  parser.add_argument('column', type=str, required=True, help='Please provide the column')
  parser.add_argument('new_text', type=str, required=True, help='Please provide the new_text')

  def put(self):
    fact_id = Fact.parser.parse_args()['fact_id']
    column = Fact.parser.parse_args()['column']
    new_text = Fact.parser.parse_args()['new_text']

    for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
            table = pd.read_csv(path, sep='\t')
            if(fact_id in table['[SKIP] UID'].values):
              table.loc[table['[SKIP] UID'] == fact_id, column] = new_text
              table.to_csv(path, sep='\t', index=False)

    return 'success'

  def __getFact(self, fact_id):
    for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
            table = pd.read_csv(path, sep='\t')
            return table.loc[table['[SKIP] UID'] == fact_id]
            