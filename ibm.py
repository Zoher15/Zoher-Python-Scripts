import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, RelationsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey="gjgHhqHI_bv16HRb0q0gsAOAx57ZUurHqOl1gr9aXJ7P",
    url="https://gateway.watsonplatform.net/natural-language-understanding/api"
)

response = natural_language_understanding.analyze(
    text='France Passes Law Saying Children Can Consent To Sex With Adults',
    features=Features(relations=RelationsOptions())).get_result()

print(json.dumps(response, indent=2))