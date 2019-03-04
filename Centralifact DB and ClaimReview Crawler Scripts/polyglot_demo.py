import polyglot
from polyglot.text import Text, Word
a="Berlusconi, quando la Lega aveva il 4% e FI-Pdl il 35%, con il suo stile e la sua intelligenza strategica garantiva tutti, consentiva alla Lega di governare tre Regioni del Nord"
ner_entities=Text(a).entities
print ner_entities