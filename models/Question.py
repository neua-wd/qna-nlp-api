import pandas as pd

from constants import QUESTION_FILE_PATH


class Question:
    def __init__(self):
        self.question_table = pd.read_csv(QUESTION_FILE_PATH, sep='\t')

    def get_row_by_id(self, question_id):
        return self.question_table[self.question_table['QuestionID']
                                   == question_id]

    def get_row_by_question(self, question):
        return self.question_table[self.question_table['question'].str.contains(
            question.lower(), case=False)]

    def sample(self):
        return self.question_table.sample()

    def add_fact_to_explanation(self, question_id, explanation_column, new_fact_id):
        question_row = self.get_row_by_id(question_id)
        current_ids = question_row[explanation_column].values[0]

        if (type(current_ids) == str):
            updated = current_ids + ' ' + new_fact_id + '|ADDED'
        else:
            updated = ' ' + new_fact_id + '|ADDED'

        question_row[explanation_column] = updated

        if (explanation_column == "explanation"):
            corresponding_column = "correct" + question_row["AnswerKey"]
            question_row[corresponding_column] = updated

        self.__save_row_to_table(question_row)

    def update_explanation(self,
                           question_id,
                           explanation_column,
                           new_facts):
        question_row = self.get_row_by_id(question_id)

        tag_map = {}
        for id_with_tag in question_row[explanation_column].values[0].split():
            pair = id_with_tag.split('|')
            tag_map[pair[0]] = pair[1]

        updated = ""
        for fact_id in new_facts:
            updated += fact_id + '|' + tag_map[fact_id] + ' '

        question_row[explanation_column] = updated

        if (explanation_column == "explanation"):
            corresponding_column = "correct" + question_row["AnswerKey"]
            question_row[corresponding_column] = updated

        self.__save_row_to_table(question_row)

    def change_answer(self, question_id, new_answer):
        question_row = self.get_row_by_id(question_id)
        question_row['AnswerKey'] = new_answer
        question_row['explanation'] = question_row['correct' + new_answer]

        self.__save_row_to_table(question_row)

    def __save_row_to_table(self, row):
        question_id = row['QuestionID'].values[0]

        self.question_table.loc[self.question_table['QuestionID']
                                == question_id] = row

        self.question_table.to_csv(QUESTION_FILE_PATH, sep='\t', index=False)
