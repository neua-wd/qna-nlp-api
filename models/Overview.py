import pandas as pd
import re
import glob

from constants import QUESTION_FILE_PATH, TABLES_DIRECTORY


class Overview:
    def find(self, question):
        return self.__get_overview_from_row(
            self.__get_row_by_question(question))


    def find_by_id(self, question_id):
        return self.__get_overview_from_row(
            self.__get_row_by_id(question_id))


    def __get_overview_from_row(self, row):
        if (len(row['question'].values) == 0): raise Exception(
            'Question does not exist')

        question_elements = re.split(' \(', row['question'].values[0])

        return {
            'question_id': row['QuestionID'].values[0],
            'question': question_elements[0],
            'choices': self.__getChoices(question_elements),
            'answer': row['AnswerKey'].values[0],
            'explanation': self.__getExplanation(row['explanation'].values[0])
        }


    def __get_row_by_question(self, question):
        table = pd.read_csv(QUESTION_FILE_PATH, sep='\t')

        return table[table['question'].str.contains(question)]


    def __get_row_by_id(self, question_id):
        table = pd.read_csv(QUESTION_FILE_PATH, sep='\t')

        return table[table['QuestionID'] == question_id]

    def __getChoices(self, question_elements):
        choices = {}
        for i in range(1, len(question_elements)):
            choice = question_elements[i]
            choices[choice[0]] = choice[3:]

        return choices


    def __getExplanation(self, ids_with_tags):
        explanation_ids = []
        explanation_rows = []
        explanations = []

        for id in ids_with_tags.split():
            explanation_ids.append(id.split('|')[0])
        
        for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
            table = pd.read_csv(path, sep='\t')
            row = table.loc[table['[SKIP] UID'].isin(explanation_ids)]
            if (row.size > 0):
                explanation_rows.append(row)

        for row in explanation_rows:
            explanation = {}
            for column in row.columns:
                value = row[column].values[0]
                if ((column == '[SKIP] UID') | ('[SKIP]' not in column)):
                    explanation[column] = value if type(value) == str else ''
            explanations.append(explanation)


        return explanations
