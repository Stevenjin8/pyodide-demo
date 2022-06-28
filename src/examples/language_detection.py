# From https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/language-detection/quickstart
# pylint: disable=await-outside-async, undefined-variable
documents = ["Ce document est rédigé en Français."]
response = (await client.detect_language(documents=documents, country_hint="us"))[0]  # type: ignore
print("Language: ", response.primary_language.name)
