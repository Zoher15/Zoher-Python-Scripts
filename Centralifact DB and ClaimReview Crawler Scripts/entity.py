# from polyglot.text import Text
# blob = "While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal."
# text = Text(blob)
# print text.entities
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
st = StanfordNERTagger('stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz',
					   'stanford-ner-2018-02-27/stanford-ner.jar',
					   encoding='utf-8')
text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'

tokenized_text = word_tokenize(text)
classified_text = st.tag(tokenized_text)

print(classified_text)