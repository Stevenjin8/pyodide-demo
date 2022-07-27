# From https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/text-analytics-for-health/quickstart
# pylint: disable=await-outside-async, undefined-variable, consider-using-f-string

################################################################################
# HEALTH #######################################################################
################################################################################

HEALTH_EXAMPLE = """
documents = [
    \"\"\"
    Patient needs to take 50 mg of ibuprofen.
    \"\"\"
]

poller = await client.begin_analyze_healthcare_entities(documents)  # type: ignore
result = await poller.result()  # type: ignore
docs = [doc async for doc in result if not doc.is_error]  # type: ignore

for idx, doc in enumerate(docs):
    for entity in doc.entities:
        print("Entity: {}".format(entity.text))
        print("...Normalized Text: {}".format(entity.normalized_text))
        print("...Category: {}".format(entity.category))
        print("...Subcategory: {}".format(entity.subcategory))
        print("...Offset: {}".format(entity.offset))
        print("...Confidence score: {}".format(entity.confidence_score))
    for relation in doc.entity_relations:
        print(
            "Relation of type: {} has the following roles".format(
                relation.relation_type
            ),
        )
        for role in relation.roles:
            print(
                "...Role '{}' with entity '{}'".format(role.name, role.entity.text),
            )
    print("------------------------------------------")"""

################################################################################
# LANGUAGE DETECTION ###########################################################
################################################################################

LANGUAGE_DETECTION_EXAMPLE = """
# From https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/text-analytics-for-health/quickstart
documents = [
  \"\"\"
  Patient needs to take 50 mg of ibuprofen.
  \"\"\"
]

poller = await client.begin_analyze_healthcare_entities(documents)  # type: ignore
result = await poller.result()  # type: ignore
docs = [doc async for doc in result if not doc.is_error]  # type: ignore

for idx, doc in enumerate(docs):
    for entity in doc.entities:
        print("Entity: {}".format(entity.text))
        print("...Normalized Text: {}".format(entity.normalized_text))
        print("...Category: {}".format(entity.category))
        print("...Subcategory: {}".format(entity.subcategory))
        print("...Offset: {}".format(entity.offset))
        print("...Confidence score: {}".format(entity.confidence_score))
    for relation in doc.entity_relations:
        print(
            "Relation of type: {} has the following roles".format(
                relation.relation_type
            ),
        )
        for role in relation.roles:
            print(
                "...Role '{}' with entity '{}'".format(role.name, role.entity.text),
            )
    print("------------------------------------------")"""

################################################################################
# PII DETECTION ################################################################
################################################################################

PII_EXAMPLE = """
documents = [
    "The employee's SSN is 859-98-0987.",
    "The employee's phone number is 555-555-5555.",
]
response = await client.recognize_pii_entities(documents, language="en")  # type: ignore
result = [doc for doc in response if not doc.is_error]
for doc in result:
    print("Redacted Text: {}".format(doc.redacted_text))
    for entity in doc.entities:
        print("Entity: {}".format(entity.text))
        print("\tCategory: {}".format(entity.category))
        print("\tConfidence Score: {}".format(entity.confidence_score))
        print("\tOffset: {}".format(entity.offset))
        print("\tLength: {}".format(entity.length))"""

################################################################################
# PII DETECTION ################################################################
################################################################################

RECEIPTS_EXAMPLE = """
with open("receipt.jpeg", "rb") as f:
    data = f.read()
poller = await client.begin_recognize_receipts(data)  # type: ignore
result = (await poller.result())[0]  # type: ignore
for k, v in result.fields.items():
    print(k, ":", v.value_data.text if v.value_data else "-")"""

################################################################################
# SENTIMENT ANALYSIS ###########################################################
################################################################################

SENTIMENT_ANALYSIS_EXAMPLE = """
documents = ["The food and service were unacceptable, but the concierge were nice"]

result = await client.analyze_sentiment(documents, show_opinion_mining=True)  # type: ignore
doc_result = [doc for doc in result if not doc.is_error]

positive_mined_opinions = []
mixed_mined_opinions = []
negative_mined_opinions = []

for document in doc_result:
    print("Document Sentiment: {}".format(document.sentiment))
    print(
        "Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
            document.confidence_scores.positive,
            document.confidence_scores.neutral,
            document.confidence_scores.negative,
        )
    )
    for sentence in document.sentences:
        print("Sentence: {}".format(sentence.text))
        print("Sentence sentiment: {}".format(sentence.sentiment))
        print(
            "Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
                sentence.confidence_scores.positive,
                sentence.confidence_scores.neutral,
                sentence.confidence_scores.negative,
            ),
        )
        print("\n")
    print("\n")"""

################################################################################
# STORAGE ######################################################################
################################################################################

STORAGE_EXAMPLE = """blob_client = BlobClient(
    account_url=client.url,  # type: ignore
    container_name="<your container name>",
    blob_name="<your blob name>",
    credential=client.credential,  # type: ignore
    transport=PyodideTransport(),  # type: ignore
)

downloader = await blob_client.download_blob()  # type: ignore
async for chunk in downloader.chunks():  # type: ignore
    print(chunk)"""

EXAMPLES = {
    "health": HEALTH_EXAMPLE,
    "language": LANGUAGE_DETECTION_EXAMPLE,
    "pii": PII_EXAMPLE,
    "receipts": RECEIPTS_EXAMPLE,
    "sentiment": SENTIMENT_ANALYSIS_EXAMPLE,
    "storage": STORAGE_EXAMPLE,
}
