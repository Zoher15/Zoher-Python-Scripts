from flair.data import Sentence
from flair.models import SequenceTagger
import pandas as pd
# data=pd.read_csv("claimreview_db.csv")
tagger=SequenceTagger.load('pos')
s=Sentence("France Passes Law Saying Children Can Consent To Sex With Adults")
tagger.predict(s)
print(s.to_tagged_string())
# data.apply(postagger,axis=1)
