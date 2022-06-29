# From https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/personally-identifiable-information/quickstart
# pylint: disable=await-outside-async, undefined-variable, consider-using-f-string
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
        print("\tLength: {}".format(entity.length))
