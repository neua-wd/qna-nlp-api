import glob
import pandas as pd
import os

from constants import TABLES_DIRECTORY


class Template:
  def find_all(self):
    column_names = {}

    for path in glob.glob(TABLES_DIRECTORY + '/*.tsv'):
      table = pd.read_csv(path, sep='\t')
      file = os.path.basename(path)
      column_names[file.split('.')[0]] = table.columns.values.tolist()

    return column_names