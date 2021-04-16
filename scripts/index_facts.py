# Script used to index the facts in the explanation bank, combining all
# the fact ids into one table, with each index corresponding to the tag
# that would be returned when invoking the most_similar method on the
# suggestions model

# This is so that the api can use the ids to query each fact when getting
# suggestions

# This should be run every time train_suggestions_model is run


import glob
import pandas as pd
from constants import TABLES_DIRECTORY

fact_ids = []
for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
    table = pd.read_csv(path, sep='\t')
    for content in table.iterrows():
        fact_ids.append((content[1]['[SKIP] UID']))

df = pd.DataFrame(fact_ids, columns=['Fact ID'])
df.to_csv('fact_ids.csv', index=True)
