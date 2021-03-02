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
        if (len(row['question'].values) == 0):
            raise Exception('Question does not exist')

        question_elements = re.split(' \(', row['question'].values[0])

        return {
            'question_id': row['QuestionID'].values[0],
            'question': question_elements[0],
            'choices': self.__get_choices(question_elements),
            'answer': row['AnswerKey'].values[0],
            'explanation': self.__get_explanation(row['explanation'].values[0]),
            'explanationA': self.__get_explanation(row['explanationA'].values[0]),
            'explanationB': self.__get_explanation(row['explanationB'].values[0]),
            'explanationC': self.__get_explanation(row['explanationC'].values[0]),
            'explanationD': self.__get_explanation(row['explanationD'].values[0]),
            'explanationE': self.__get_explanation(row['explanationE'].values[0]),
        }

    def __get_row_by_question(self, question):
        table = pd.read_csv(QUESTION_FILE_PATH, sep='\t')

        return table[table['question'].str.contains(question)]

    def __get_row_by_id(self, question_id):
        table = pd.read_csv(QUESTION_FILE_PATH, sep='\t')

        return table[table['QuestionID'] == question_id]

    def __get_choices(self, question_elements):
        choices = {}
        for i in range(1, len(question_elements)):
            choice = question_elements[i]
            choices[choice[0]] = choice[3:]

        return choices

    def __get_explanation(self, ids_with_tags):
        if type(ids_with_tags) != str:
            return []

        explanation_ids = []
        explanation_rows = []
        explanations = []

        for id in ids_with_tags.split():
            explanation_ids.append(id.split('|')[0])

        for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
            table = pd.read_csv(path, sep='\t')
            for explanation_id in explanation_ids:
                row = table.loc[table['[SKIP] UID'] == explanation_id]
                if (row.size > 0):
                    explanation_rows.append(row)

        for row in explanation_rows:
            explanation = {}
            for column in row.columns:
                for i in range(row[column].size):
                    value = row[column].values[i]
                    if ((column == '[SKIP] UID') | ('[SKIP]' not in column)):
                        explanation[column] = value if type(
                            value) == str else ''
            explanations.append(explanation)

        return explanations
