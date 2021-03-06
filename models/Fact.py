from constants import TABLES_DIRECTORY, QUESTION_FILE_PATH, ABSTRACTIVE_TAGS
import glob
import pandas as pd
import uuid
from nltk import PorterStemmer, WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords

from models.Question import Question


class Fact:
    def __init__(self, model=None, fact_ids=None):
        self.model = model
        self.fact_ids = fact_ids

    def get_facts_by_ids(self, ids):
        facts = {}
        for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
            table = pd.read_csv(path, sep='\t')
            for explanation_id in ids:
                fact_row = table.loc[table['[SKIP] UID'] == explanation_id]
                if (fact_row.size > 0):
                    facts[fact_row['[SKIP] UID'].values[0]
                          ] = self.__get_explanation_from_fact(fact_row)

        return self.__get_correct_order(ids, facts)

        # Add new fact to the corresponsing fact table
        # and add the id to the question's explanation list
    def add(self, fact_table_name, question_id, explanation_column, new_fact):
        fact_table_path = TABLES_DIRECTORY + "/" + fact_table_name + '.tsv'
        new_fact_id = str(uuid.uuid4())

        self.__add_new_fact(fact_table_path, new_fact, new_fact_id)
        Question().add_fact_to_explanation(question_id,
                                           explanation_column,
                                           new_fact_id)

    def update(self, edited_fact):
        fact_id = edited_fact['[SKIP] UID']

        for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
            table = pd.read_csv(path, sep='\t')

            if(fact_id in table['[SKIP] UID'].values):
                for column in edited_fact:
                    table.loc[table['[SKIP] UID'] == fact_id, column] = (
                        edited_fact[column])

                table.to_csv(path, sep='\t', index=False)

    def categorize(self, facts):
        abstracion = []
        unification = {}

        for fact in facts:
            if ABSTRACTIVE_TAGS & fact.keys():
                abstracion.append(fact)
            elif len(unification) == 0:
                unification = fact

        return {
            "abstraction": abstracion,
            "unification": unification
        }

    def get_similar(self, sentence):
        tokens = word_tokenize(sentence.lower())

        normalized_tokens = []
        for word in tokens:
            if word not in stopwords.words('english'):
                word = WordNetLemmatizer().lemmatize(word)
                word = PorterStemmer().stem(word)
                normalized_tokens.append(word)

        vector = self.model.infer_vector(normalized_tokens)
        most_similar = self.model.docvecs.most_similar(positive=[vector],
                                                       topn=12)

        ids = []
        for sentence in most_similar:
            ids.append(self.fact_ids['Fact ID'][sentence[0]])

        return self.get_facts_by_ids(ids)

    def __get_correct_order(self, ids, facts):
        ordered = []
        for fact_id in ids:
            if (fact_id in facts):
                ordered.append(facts[fact_id])

        return ordered

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

    def __get_explanation_from_fact(self, fact_row):
        explanation = {}
        for column in fact_row.columns:
            for i in range(fact_row[column].size):
                value = fact_row[column].values[i]
                if ((column == '[SKIP] UID') | ('[SKIP]' not in column)):
                    explanation[column] = value if type(
                        value) == str else ''

        return explanation
