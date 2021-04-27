# Script used to train a Doc2Vec model

# Each fact/sentence in the explanation bank is treated as a document
# The model is then saved for later use (getting suggestions)

# index_facts.py should also be run after every training


from nltk import PorterStemmer, WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import glob
from constants import TABLES_DIRECTORY
import pandas as pd


def filter_func(header):
    return "[SKIP]" not in header


sentences = []
normalized_sentences = []

for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
    table = pd.read_csv(path, sep='\t')

    for content in table.iterrows():
        row = content[1].to_dict()
        filtered = filter(filter_func, row)

        sentence = ""
        normalized_sentence = []

        for key in filtered:
            value = row[key]
            if type(value) == str:
                tokenized = word_tokenize(value)
                normalized = []
                for word in tokenized:
                    if sentence == "":
                        sentence += word
                    else:
                        sentence += ' ' + word

                    if word not in stopwords.words('english'):
                        word = WordNetLemmatizer().lemmatize(word)
                        word = PorterStemmer().stem(word)
                        normalized.append(word)

                normalized_sentence.extend(tokenized)

        sentences.append(sentence)
        normalized_sentences.append(normalized_sentence)

tagged_normalized = [TaggedDocument(d, [i])
                     for i, d in enumerate(normalized_sentences)]
model = Doc2Vec(tagged_normalized, vector_size=200,
                window=10, min_count=1, epochs=100)
model.save('suggestions.model')
