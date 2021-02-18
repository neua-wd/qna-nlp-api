from flask_restful import Resource
import pandas as pd
import re


class Overview(Resource):
    def get(self, id):
        questions = pd.read_csv('./questions.dev.tsv', sep='\t')

        row = questions.loc[questions['QuestionID'] == id]
        question_elements = re.split('\(', row['question'].values[0])

        choices = {}
        for i in range(1, len(question_elements)):
            choice = question_elements[i]
            choices[choice[0]] = choice[3:]

        overview = {"question": question_elements[0]}
        overview['answer'] = row['AnswerKey'].values[0]
        overview['choices'] = choices

        return overview
