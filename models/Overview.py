import pandas as pd
import re
import glob

from constants import QUESTION_FILE_PATH, TABLES_DIRECTORY


class Overview:
    def __init__(self):
        self.question_table = pd.read_csv(QUESTION_FILE_PATH, sep='\t')

    def find(self, question):
        row = self.question_table[self.question_table['question'].str.contains(
            question)]

        return self.__get_overview_from_row(row)

    def find_by_id(self, question_id):
        row = self.question_table[self.question_table['QuestionID']
                                  == question_id]

        return self.__get_overview_from_row(row)

    def sample(self):
        sample = self.question_table.sample()
        return self.__get_overview_from_row(sample)

    def update_explanation(self,
                           question_id,
                           explanation_column,
                           new_facts):
        question_row = self.question_table[self.question_table['QuestionID']
                                           == question_id]
        old_explanation = question_row[explanation_column].values[0].split()

        new_facts_with_tags = []
        for fact_id in new_facts:
            new_facts_with_tags.append(
                ''.join(
                    [id_with_tag for id_with_tag in old_explanation if fact_id in id_with_tag]))

        self.question_table.loc[self.question_table['QuestionID']
                                == question_id, explanation_column] = ' '.join(new_facts_with_tags)

        self.question_table.to_csv(QUESTION_FILE_PATH, sep='\t', index=False)

        return self.__get_overview_from_row(
            self.question_table[self.question_table['QuestionID']
                                == question_id])

    def __get_overview_from_row(self, row):
        if (len(row['question'].values) == 0):
            raise Exception('Question does not exist')

        question_elements = re.split(' \(', row['question'].values[0])
        answer = row['AnswerKey'].values[0]

        overview = {
            'question_id': row['QuestionID'].values[0],
            'question': question_elements[0],
            'choices': self.__get_choices(question_elements),
            'answer': answer,
            'explanation': self.__get_explanation(row['explanation'].values[0])
        }

        for choice in ['A', 'B', 'C', 'D', 'E']:
            if (answer != choice):
                key = 'incorrect' + choice
                overview[key] = self.__get_explanation(row[key].values[0])

        return overview

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
        explanations = {}

        for fact_id in ids_with_tags.split():
            explanation_ids.append(fact_id.split('|')[0])

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

            explanations[row['[SKIP] UID'].values[0]] = explanation

        return self.__get_correct_order(explanation_ids, explanations)

    def __get_correct_order(self, explanation_ids, explanations):
        ordered = []
        for explanation_id in explanation_ids:
            if (explanation_id in explanations):
                ordered.append(explanations[explanation_id])

        return ordered
