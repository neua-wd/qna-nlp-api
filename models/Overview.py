import pandas as pd
import re
import glob

from constants import QUESTION_FILE_PATH, TABLES_DIRECTORY

from models.Fact import Fact


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
        question_row = self.__get_row_by_id(question_id)
        old_explanation = question_row[explanation_column].values[0].split()

        new_facts_with_tags = []
        for fact_id in new_facts:
            new_facts_with_tags.append(
                ''.join(
                    [id_with_tag for id_with_tag in old_explanation if fact_id in id_with_tag]))

        question_row[explanation_column] = ' '.join(new_facts_with_tags)

        self.__save_row_to_table(question_row, question_id)

        return self.__get_overview_from_row(question_row)

    def update_answer(self, question_id, new_answer):
        question_row = self.__get_row_by_id(question_id)
        question_row['AnswerKey'] = new_answer

        correct_explanation = 'correct' + new_answer
        question_row['explanation'] = question_row[correct_explanation]

        self.__save_row_to_table(question_row, question_id)

        return self.__get_overview_from_row(question_row)

    def add_fact(self, question_id, explanation_column, new_fact_id):
        question_row = self.__get_row_by_id(question_id)

        current_ids = question_row[explanation_column].values[0]
        if (type(current_ids) == str):
            updated = current_ids + ' ' + new_fact_id + '|ADDED'
        else:
            updated = ' ' + new_fact_id + '|ADDED'

        question_row[explanation_column] = updated

        self.__save_row_to_table(question_row, question_id)

        return self.__get_overview_from_row(question_row)

    def __get_row_by_id(self, question_id):
        return self.question_table[self.question_table['QuestionID']
                                   == question_id]

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

        for fact_id in ids_with_tags.split():
            explanation_ids.append(fact_id.split('|')[0])

        return Fact().get_facts_by_ids(explanation_ids)

    def __save_row_to_table(self, row, question_id):
        self.question_table.loc[self.question_table['QuestionID']
                                == question_id] = row
        self.question_table.to_csv(QUESTION_FILE_PATH, sep='\t', index=False)
