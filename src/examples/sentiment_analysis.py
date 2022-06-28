# https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/sentiment-opinion-mining/quickstart
# pylint: disable=await-outside-async, undefined-variable
documents = ["The food and service were unacceptable, but the concierge were nice"]

result = await client.analyze_sentiment(documents, show_opinion_mining=True)  # type: ignore
doc_result = [doc for doc in result if not doc.is_error]

positive_reviews = [doc for doc in doc_result if doc.sentiment == "positive"]
negative_reviews = [doc for doc in doc_result if doc.sentiment == "negative"]

positive_mined_opinions = []
mixed_mined_opinions = []
negative_mined_opinions = []

for document in doc_result:
    print("Document Sentiment: {}".format(document.sentiment))
    print(
        "Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \\n".format(
            document.confidence_scores.positive,
            document.confidence_scores.neutral,
            document.confidence_scores.negative,
        )
    )
    for sentence in document.sentences:
        print("Sentence: {}".format(sentence.text))
        print("Sentence sentiment: {}".format(sentence.sentiment))
        print(
            "Sentence score:\\nPositive={0:.2f}\\nNeutral={1:.2f}\\nNegative={2:.2f}\\n".format(
                sentence.confidence_scores.positive,
                sentence.confidence_scores.neutral,
                sentence.confidence_scores.negative,
            ),
        )
        for mined_opinion in sentence.mined_opinions:
            target = mined_opinion.target
            print(
                "......'{}' target '{}'".format(target.sentiment, target.text),
            )
            print(
                "......Target score:\\n......Positive={0:.2f}\\n......Negative={1:.2f}\\n".format(
                    target.confidence_scores.positive,
                    target.confidence_scores.negative,
                ),
            )
            for assessment in mined_opinion.assessments:
                print(
                    "......'{}' assessment '{}'".format(
                        assessment.sentiment, assessment.text
                    ),
                )
                print(
                    "......Assessment score:\\n......Positive={0:.2f}\\n......Negative={1:.2f}\\n".format(
                        assessment.confidence_scores.positive,
                        assessment.confidence_scores.negative,
                    ),
                )
        print("\\n")
    print("\\n")
