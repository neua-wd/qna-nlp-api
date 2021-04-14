import pandas as pd
import re
import glob

from constants import QUESTION_FILE_PATH, TABLES_DIRECTORY

from models.Fact import Fact
from models.Question import Question


class Overview:
    def get_overview_from_row(self, row):
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
