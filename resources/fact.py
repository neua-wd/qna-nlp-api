from flask_restful import Resource, reqparse
import glob
import pandas as pd
from constants import TABLES_DIRECTORY

class Fact(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('edited_fact', type=dict, required=True, help='Please provide the edited fact')

  def put(self):
    edited_fact = Fact.parser.parse_args()['edited_fact']
    fact_id = edited_fact['[SKIP] UID']

    for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
            table = pd.read_csv(path, sep='\t')
            if(fact_id in table['[SKIP] UID'].values):
              # row = table.loc[table['[SKIP] UID'] == fact_id]
              for column in edited_fact:
                table.loc[table['[SKIP] UID'] == fact_id, column] = edited_fact[column]
              table.to_csv(path, sep='\t', index=False)

    return 'success'

  def __getFact(self, fact_id):
    for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
            table = pd.read_csv(path, sep='\t')
            return table.loc[table['[SKIP] UID'] == fact_id]
            