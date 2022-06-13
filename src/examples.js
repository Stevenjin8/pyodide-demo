const EXAMPLES = {
  sentimentAnalysis: `# https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/sentiment-opinion-mining/quickstart
output_file = StringIO()
documents = [
    "The food and service were unacceptable, but the concierge were nice"
]

result = await client.analyze_sentiment(documents, show_opinion_mining=True)
doc_result = [doc for doc in result if not doc.is_error]

positive_reviews = [doc for doc in doc_result if doc.sentiment == "positive"]
negative_reviews = [doc for doc in doc_result if doc.sentiment == "negative"]

positive_mined_opinions = []
mixed_mined_opinions = []
negative_mined_opinions = []

for document in doc_result:
    print("Document Sentiment: {}".format(document.sentiment), file=output_file)
    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \\n".format(
        document.confidence_scores.positive,
        document.confidence_scores.neutral,
        document.confidence_scores.negative,
    ), file=output_file)
    for sentence in document.sentences:
        print("Sentence: {}".format(sentence.text), file=output_file)
        print("Sentence sentiment: {}".format(sentence.sentiment), file=output_file)
        print("Sentence score:\\nPositive={0:.2f}\\nNeutral={1:.2f}\\nNegative={2:.2f}\\n".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        ), file=output_file)
        for mined_opinion in sentence.mined_opinions:
            target = mined_opinion.target
            print("......'{}' target '{}'".format(target.sentiment, target.text), file=output_file)
            print("......Target score:\\n......Positive={0:.2f}\\n......Negative={1:.2f}\\n".format(
                target.confidence_scores.positive,
                target.confidence_scores.negative,
            ), file=output_file)
            for assessment in mined_opinion.assessments:
                print("......'{}' assessment '{}'".format(assessment.sentiment, assessment.text), file=output_file)
                print("......Assessment score:\\n......Positive={0:.2f}\\n......Negative={1:.2f}\\n".format(
                    assessment.confidence_scores.positive,
                    assessment.confidence_scores.negative,
                ), file=output_file)
        print("\\n", file=output_file)
    print("\\n", file=output_file)
output_file.seek(0)
output_file.read().strip()`,

  languageDetection: `# From https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/language-detection/quickstart
output_file = StringIO()
documents = ["Ce document est rédigé en Français."]
response = (await client.detect_language(documents = documents, country_hint = 'us'))[0]
print("Language: ", response.primary_language.name, file=output_file)
output_file.seek(0)
output_file.read().strip()`,

  health: `# From https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/text-analytics-for-health/quickstart
output_file = StringIO()
documents = [
  """
  Patient needs to take 50 mg of ibuprofen.
  """
]

poller = await client.begin_analyze_healthcare_entities(documents)
result = await poller.result()

docs = [doc async for doc in result if not doc.is_error]

for idx, doc in enumerate(docs):
  for entity in doc.entities:
      print("Entity: {}".format(entity.text), file=output_file)
      print("...Normalized Text: {}".format(entity.normalized_text), file=output_file)
      print("...Category: {}".format(entity.category), file=output_file)
      print("...Subcategory: {}".format(entity.subcategory), file=output_file)
      print("...Offset: {}".format(entity.offset), file=output_file)
      print("...Confidence score: {}".format(entity.confidence_score), file=output_file)
  for relation in doc.entity_relations:
      print("Relation of type: {} has the following roles".format(relation.relation_type), file=output_file)
      for role in relation.roles:
          print("...Role '{}' with entity '{}'".format(role.name, role.entity.text), file=output_file)
  print("------------------------------------------", file=output_file)
output_file.seek(0)
output_file.read().strip()`,

  pii: `# From https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/personally-identifiable-information/quickstart
output_file = StringIO()
documents = [
    "The employee's SSN is 859-98-0987.",
    "The employee's phone number is 555-555-5555."
]
response = await client.recognize_pii_entities(documents, language="en")
result = [doc for doc in response if not doc.is_error]
for doc in result:
    print("Redacted Text: {}".format(doc.redacted_text), file=output_file)
    for entity in doc.entities:
        print("Entity: {}".format(entity.text), file=output_file)
        print("\\tCategory: {}".format(entity.category), file=output_file)
        print("\\tConfidence Score: {}".format(entity.confidence_score), file=output_file)
        print("\\tOffset: {}".format(entity.offset), file=output_file)
        print("\\tLength: {}".format(entity.length), file=output_file)
output_file.seek(0)
output_file.read().strip()`,
};

export default function getExamples() {
  return EXAMPLES;
}
