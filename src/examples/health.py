# From https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/text-analytics-for-health/quickstart
# pylint: disable=await-outside-async, undefined-variable, consider-using-f-string
documents = [
    """
  Patient needs to take 50 mg of ibuprofen.
  """
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
    print("------------------------------------------")
