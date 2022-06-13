import loadPyodide from 'pyodide';
const output = document.getElementById('output');
output.value = 'Initializing...\n';
const code = document.getElementById('code');

const select = document.getElementById('example');
const run = document.getElementById('run');
const clear = document.getElementById('clear');
const buttons = [select, run, clear];

async function initEnv(pyodide) {
  await pyodide.runPythonAsync(`
        import js
        import micropip
        from pyodide.http import pyfetch

        # Install packages
        await micropip.install("azure-ai-textanalytics")
        await micropip.install("python-dotenv")
        from dotenv import load_dotenv
        import os
        try:
          response = await pyfetch("http://localhost:8000/.env")
          with open(".env", "wb") as f:
              f.write(await response.bytes())
        
          # Load keys like this so I can develop fast without hardcoding
          # sensitive information. In the future, these will be prompts.
          load_dotenv()
          AZ_KEY = os.getenv("AZ_KEY1")
          AZ_ENDPOINT = os.getenv("AZ_ENDPOINT")
        except Exception:
            AZ_KEY = js.prompt("Please enter your textanalytics key: ")
            AZ_ENDPOINT = js.prompt("Please enter your textanalytics endpoint: ")

        from collections.abc import AsyncIterator
        from azure.ai.textanalytics.aio import TextAnalyticsClient
        from azure.core.credentials import AzureKeyCredential
        from azure.core.pipeline.transport._requests_asyncio import AsyncioRequestsTransport
        from azure.core.rest._http_response_impl_async import AsyncHttpResponseImpl

        class PyodideTransport(AsyncioRequestsTransport):
            """Implements a basic HTTP sender using the pyodide javascript fetch api."""

            async def send(self, request, **kwargs):  # type: ignore
                """Send request object according to configuration.

                :param request: The request object to be sent.
                :type request: ~azure.core.pipeline.transport.HttpRequest
                :return: An HTTPResponse object.
                :rtype: ~azure.core.pipeline.transport.HttpResponse
                """
                endpoint = request.url
                request_headers = dict(request.headers)
                init = {
                    "method": request.method,
                    "headers": request_headers,
                    "body": request.data,
                    "files": request.files,
                    "verify": kwargs.pop("connection_verify", self.connection_config.verify),
                    # "timeout": timeout,
                    "cert": kwargs.pop("connection_cert", self.connection_config.cert),
                    "allow_redirects": False,
                    **kwargs,
                }
                response = await pyfetch(endpoint, **init)
                headers = dict(response.js_response.headers)
                res = PyodideTransportResponse(
                    request=request,
                    internal_response=response,
                    block_size=self.connection_config.data_block_size,
                    status_code=response.status,
                    reason=response.status_text,
                    content_type=headers.get("content-type"),
                    headers=headers,
                    stream_download_generator=PyodideStreamDownloadGenerator,
                )
                await res.read()
                return res


        class PyodideTransportResponse(AsyncHttpResponseImpl):
            async def close(self):
                """This is kinda weird but AsyncHttpResponseImpl assumed that
                the internal response is a requests.Reponse object (I think).
                FIXME
                """
                self._is_closed = True


        class PyodideStreamDownloadGenerator(AsyncIterator):
            """Simple stream download generator that returns the contents of
            a request."""

            def __init__(self, response: PyodideTransportResponse, **__) -> None:
                self.request = response.request
                self.response = response
                self.done = False

            def __len__(self):
                return 1

            async def __anext__(self):
                if self.done:
                    raise StopAsyncIteration()
                self.done = True
                return await self.response._internal_response.bytes()
      `);
}

/**
 * Initialize python environment.
 */
async function init(pyodide) {
  await pyodide.loadPackage('micropip');
  await initEnv(pyodide);
  updateExample();
}

/**
 * Create a text analytics client in the python namespace
 */
function createClient(pyodide) {
  pyodide.runPython(`
            from azure.ai.textanalytics.aio import TextAnalyticsClient
            from azure.core.credentials import AzureKeyCredential

            client = TextAnalyticsClient(
                endpoint=AZ_ENDPOINT,
                credential=AzureKeyCredential(AZ_KEY),
                transport=PyodideTransport(),
            )
        `);
}

/**
 * Enable user input buttons.
 */
function enableButtons() {
  for (const elem of buttons) {
    elem.disabled = false;
  }
}

/**
 * Disable user input buttons.
 */
function disableButtons() {
  for (const elem of buttons) {
    elem.disabled = true;
  }
}

/**
 * Add formatted multi-line code to the output.
 */
function addToOutput(s) {
  let consoleCode = code.value.split('\n').join('\n... ');
  output.value += '>>> ' + consoleCode + '\n' + s + '\n';
  // Scrolls the output to the bottom.
  output.scrollTop = output.scrollHeight;
}

/**
 * Clears the output box.
 */
function clearConsole() {
  output.value = '';
}

// init Pyodide
async function main() {
  let pyodide = await loadPyodide();
  await init(pyodide);
  createClient(pyodide);
  enableButtons();
  output.value += 'Ready!\n';
  return pyodide;
}
let pyodideReadyPromise = main();

async function evaluatePython() {
  disableButtons();
  let pyodide = await pyodideReadyPromise;
  try {
    let output = await pyodide.runPythonAsync(code.value);
    addToOutput(output);
  } catch (err) {
    addToOutput(err);
  }
  enableButtons();
}

/**
 * Input the selected example into the input box.
 */
function updateExample() {
  let key = select.value;
  code.value = EXAMPLES[key];
  code.setAttribute('rows', EXAMPLES[key].split(/\r\n|\r|\n/).length);
}

EXAMPLES = {};

EXAMPLES.sentimentAnalysis = `output = []
documents = ["I had the best day of my life. I wish you were there with me."]
response = (await client.analyze_sentiment(documents=documents))[0]
output.append("Document Sentiment: {}\\n".format(response.sentiment))
output.append("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \\n".format(
    response.confidence_scores.positive,
    response.confidence_scores.neutral,
    response.confidence_scores.negative,
))
"\\n".join(output)`;

EXAMPLES.languageDetection = `output =[] 
documents = [
    """
    The concierge Paulette was extremely helpful. Sadly when we arrived the elevator was broken, but with Paulette's help we barely noticed this inconvenience.
    She arranged for our baggage to be brought up to our room with no extra charge and gave us a free meal to refurbish all of the calories we lost from
    walking up the stairs :). Can't say enough good things about my experience!
    """,
    """
    最近由于工作压力太大，我们决定去富酒店度假。那儿的温泉实在太舒服了，我跟我丈夫都完全恢复了工作前的青春精神！加油！
    """
]
async with client:
    result = await client.detect_language(documents)

reviewed_docs = [doc for doc in result if not doc.is_error]

output.append("Let's see what language each review is in!\\n")

for idx, doc in enumerate(reviewed_docs):
    output.append("Review #{} is in '{}', which has ISO639-1 name '{}'\\n".format(
        idx, doc.primary_language.name, doc.primary_language.iso6391_name
    ))
    if doc.is_error:
        output.append(" ".join([str(doc.id), str(doc.error)]))
"\\n".join(output)`;

EXAMPLES.health = `output = []
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
      output.append("Entity: {}".format(entity.text))
      output.append("...Normalized Text: {}".format(entity.normalized_text))
      output.append("...Category: {}".format(entity.category))
      output.append("...Subcategory: {}".format(entity.subcategory))
      output.append("...Offset: {}".format(entity.offset))
      output.append("...Confidence score: {}".format(entity.confidence_score))
  for relation in doc.entity_relations:
      output.append("Relation of type: {} has the following roles".format(relation.relation_type))
      for role in relation.roles:
          output.append("...Role '{}' with entity '{}'".format(role.name, role.entity.text))
  output.append("------------------------------------------")
"\\n".join(output)`;
