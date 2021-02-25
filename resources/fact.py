from flask_restful import Resource, reqparse
import glob
import pandas as pd
import uuid
from constants import TABLES_DIRECTORY

class Fact(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('edited_fact', type=dict, help='Please provide the edited fact')
  parser.add_argument('table_name', type=str, help='Please provide the table name')
  parser.add_argument('new_fact', type=dict, help='Please provide the new fact')

  def post(self):
    table_name = Fact.parser.parse_args()['table_name']
    new_fact = Fact.parser.parse_args()['new_fact']
    table_path = TABLES_DIRECTORY + "/" + table_name + '.tsv'
    table = pd.read_csv(table_path, sep='\t')

    new_row = {}
    for column_name in new_fact:
      new_row[column_name] = new_fact[column_name]
    
    new_row['[SKIP] UID'] = uuid.uuid4()

    updated_table = table.append(new_row, ignore_index=True)
    updated_table.to_csv(table_path, sep='\t', index=False)

    return 'success'

  def put(self):
    edited_fact = Fact.parser.parse_args()['edited_fact']
    fact_id = edited_fact['[SKIP] UID']

    for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
      table = pd.read_csv(path, sep='\t')

      if(fact_id in table['[SKIP] UID'].values):
        for column in edited_fact:
          table.loc[table['[SKIP] UID'] == fact_id, column] = edited_fact[column]

        table.to_csv(path, sep='\t', index=False)

    return 'success'

  def __getFact(self, fact_id):
    for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
            table = pd.read_csv(path, sep='\t')
            return table.loc[table['[SKIP] UID'] == fact_id]
            