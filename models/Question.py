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
            question)]

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
        old_explanation = question_row[explanation_column].values[0].split()

        new_facts_with_tags = []
        for fact_id in new_facts:
            new_facts_with_tags.append(
                ''.join(
                    [id_with_tag for id_with_tag in old_explanation if fact_id in id_with_tag]))

        updated = ' '.join(new_facts_with_tags)

        question_row[explanation_column] = updated

        if (explanation_column == "explanation"):
            corresponding_column = "correct" + question_row["AnswerKey"]
            question_row[corresponding_column] = updated

        self.__save_row_to_table(question_row)

    def change_answer(self, question_id, new_answer):
        question_row = self.get_row_by_id(question_id)
        question_row['AnswerKey'] = new_answer

        correct_explanation = 'correct' + new_answer
        question_row['explanation'] = question_row[correct_explanation]

        self.__save_row_to_table(question_row)

    def __save_row_to_table(self, row):
        question_id = row['QuestionID'].values[0]

        self.question_table.loc[self.question_table['QuestionID']
                                == question_id] = row

        self.question_table.to_csv(QUESTION_FILE_PATH, sep='\t', index=False)
