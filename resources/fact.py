from flask_restful import Resource, reqparse
import glob
import pandas as pd
import uuid
from constants import TABLES_DIRECTORY
from constants import QUESTION_FILE_PATH

class Fact(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('edited_fact', type=dict, help='Please provide the edited fact')
  parser.add_argument('table_name', type=str, help='Please provide the table name')
  parser.add_argument('to_question', type=str, help='Please provide the question ID')
  parser.add_argument('new_fact', type=dict, help='Please provide the new fact')

  def post(self):
    fact_table_name = Fact.parser.parse_args()['table_name']
    question_id = Fact.parser.parse_args()['to_question']
    new_fact = Fact.parser.parse_args()['new_fact']
    fact_table_path = TABLES_DIRECTORY + "/" + fact_table_name + '.tsv'
    new_fact_id = str(uuid.uuid4())

    self.__addNewFact(fact_table_path, new_fact, new_fact_id)
    self.__addFactToExplanation(question_id, new_fact_id)

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
            

  # Add the new fact to the corresponding fact table
  def __addNewFact(self, fact_table_path, new_fact, new_fact_id):
    fact_table = pd.read_csv(fact_table_path, sep='\t')

    new_row = {}
    for column_name in new_fact:
      new_row[column_name] = new_fact[column_name]
    new_row['[SKIP] UID'] = new_fact_id
    updated_fact_table = fact_table.append(new_row, ignore_index=True)

    updated_fact_table.to_csv(fact_table_path, sep='\t', index=False)


  # Add the id of the new fact to the list of facts for the question's explanation
  def __addFactToExplanation(self, question_id, new_fact_id):
    questions_table = pd.read_csv(QUESTION_FILE_PATH, sep='\t')
    question_row = questions_table[questions_table['QuestionID'] == question_id]
    questions_table.loc[questions_table['QuestionID'] == question_id, 'explanation'] = question_row['explanation'].values[0] + ' ' + new_fact_id

    questions_table.to_csv(QUESTION_FILE_PATH, sep='\t', index=False)