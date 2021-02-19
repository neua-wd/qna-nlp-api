from flask_restful import Resource, reqparse
import pandas as pd
import re
import glob
import numpy as np
from constants import QUESTION_FILE_PATH, TABLES_DIRECTORY

class Overview(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('question', type=str, required=True, help='Please provide the question')

    def get(self):
        row = self.__getRow(Overview.parser.parse_args()['question'])

        question_elements = re.split('\(', row['question'].values[0])
        choices = self.__getChoices(question_elements)
        explanation = self.__getExplanation(row['explanation'].values[0])
        
        overview = {"question": question_elements[0]}
        overview['answer'] = row['AnswerKey'].values[0]
        overview['choices'] = choices
        overview['explanation'] = explanation

        return overview


    def __getRow(self, question):
        table = pd.read_csv(QUESTION_FILE_PATH, sep='\t')

        return table[table['question'].str.contains(question)]


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
            explanation_dict = {}
            for column in row.columns:
                value = row[column].values[0]
                if (type(value) == str):
                    if ('[SKIP]' not in column):
                        # if ('[FILL]' in column):
                        #     explanation_dict[column] = column
                        # else:
                        explanation_dict[column] = value
            explanations.append(explanation_dict)


        return explanations
