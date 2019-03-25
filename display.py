# from IPython.display import display
from graphviz import Source
import itertools
import pandas as pd
import re
import sys


args = list(itertools.filterfalse(lambda x: re.match('^--', x), sys.argv))

data = pd.read_csv(args[1])

print(data.iloc[0]['deps_text'])
