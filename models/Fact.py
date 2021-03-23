import glob
import pandas as pd
import uuid

from constants import TABLES_DIRECTORY, QUESTION_FILE_PATH


class Fact:
    # Add new fact to the corresponsing fact table
    # and add the id to the question's explanation list
    def add(self, fact_table_name, question_id, explanation_column, new_fact):
        fact_table_path = TABLES_DIRECTORY + "/" + fact_table_name + '.tsv'
        new_fact_id = str(uuid.uuid4())

        self.__add_new_fact(fact_table_path, new_fact, new_fact_id)
        self.__add_fact_to_explanation(
            question_id, new_fact_id, explanation_column)

    def update(self, edited_fact):
        fact_id = edited_fact['[SKIP] UID']

        for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
            table = pd.read_csv(path, sep='\t')

            if(fact_id in table['[SKIP] UID'].values):
                for column in edited_fact:
                    table.loc[table['[SKIP] UID'] == fact_id, column] = (
                        edited_fact[column])

                table.to_csv(path, sep='\t', index=False)

    # return some random facts (mock data) for now
    def get_similar(self):
        table_name = 'ACTION'
        fact_table_path = TABLES_DIRECTORY + "/" + table_name + '.tsv'
        fact_table = pd.read_csv(fact_table_path, sep='\t')

        similar = []
        for row in fact_table.head(10).to_dict(orient='rows'):
            fact = {}
            for (key, value) in row.items():
                if type(value) == str:
                    fact[key] = value
            similar.append({table_name: fact})

        return similar

    # Add the new fact to the corresponding fact table
    def __add_new_fact(self, fact_table_path, new_fact, new_fact_id):
        try:
            fact_table = pd.read_csv(fact_table_path, sep='\t')
        except FileNotFoundError:
            raise Exception('Table with the given name does not exist')

        new_row = {}
        for column_name in new_fact:
            new_row[column_name] = new_fact[column_name]
        new_row['[SKIP] UID'] = new_fact_id
        updated_fact_table = fact_table.append(new_row, ignore_index=True)

        updated_fact_table.to_csv(fact_table_path, sep='\t', index=False)

    # Add the id of the new fact to question's explanation list
    def __add_fact_to_explanation(self,
                                  question_id,
                                  new_fact_id,
                                  explanation_column):
        questions = pd.read_csv(QUESTION_FILE_PATH, sep='\t')

        question_row = (questions[questions['QuestionID'] == question_id])
        if type(question_row[explanation_column].values[0]) == str:
            existing_explanation = question_row[explanation_column].values[0]
        else:
            existing_explanation = ''

        if (len(question_row.values) == 0):
            raise Exception('Question with given ID does not exist')

        questions.loc[questions['QuestionID'] == question_id, explanation_column] = (
            existing_explanation + ' ' + new_fact_id + '|ADDED')

        questions.to_csv(QUESTION_FILE_PATH, sep='\t', index=False)
