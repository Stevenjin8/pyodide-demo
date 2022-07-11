# pyright: reportMissingImports=false, reportUndefinedVariable=false
# pylint: disable=import-error, no-name-in-module
import js
import pyodide
from azure.ai.formrecognizer.aio import FormRecognizerClient
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.pipeline.transport._pyodide import PyodideTransport
from azure.storage.blob.aio import BlobServiceClient

from examples import EXAMPLES

EXAMPLES = EXAMPLES.to_py()
get_element_by_id = js.document.getElementById
USER_INPUT_CLASS_NAME = "user-input"
CONSOLE_OUTPUT = get_element_by_id("output")
CODE = get_element_by_id("code")
KEY_INPUT = get_element_by_id("key")
ENDPOINT_INPUT = get_element_by_id("endpoint")
CLIENT_TYPE_SELECT = get_element_by_id("client-type")
FILE_UPLOAD = get_element_by_id("file-upload")
EXAMPLE_SELECT = get_element_by_id("example")
TOGGLE_DOCS = get_element_by_id("toggle-docs")

client = None  # pylint: disable=invalid-name


def read_file_async(file):
    """Return a promise that resolves to the contents of a file.
    See:
    https://stackoverflow.com/questions/34495796/javascript-promises-with-filereader
    """

    def callback(resolve, reject):
        reader = js.FileReader.new()
        reader.onload = lambda *_: resolve(reader.result)
        reader.onerror = reject
        reader.readAsArrayBuffer(file)

    return js.Promise.new(pyodide.create_once_callable(callback))


async def save_files(*_):
    """Save file to virtual file system from the file upload input."""
    files = FILE_UPLOAD.files.object_values()
    for file in files:
        with open(file.name, "wb") as f:
            f.write((await read_file_async(file)).to_bytes())
        print_to_console_output(f"Uploaded {file.name} successfully!")
    FILE_UPLOAD.value = ""


def toggle_inputs(value=None):
    """Toggle user inputs on and off. Note that `value` sets the `disabled` attribute
    of inputs, so to enable all inputs, you would call `toggle_inputs(False)`.
    """
    for element in js.document.getElementsByClassName(USER_INPUT_CLASS_NAME):
        element.disabled = not element.disabled if value is None else value


def add_code_to_console_output(code: str):
    """Add nicely formatted code to console output."""
    code = "\n... ".join(code.strip().split("\n"))
    CONSOLE_OUTPUT.value += "".join((">>> ", code, "\n"))


def print_to_console_output(content: any):
    """print content to console output and scroll to the bottom."""
    content = str(content)
    CONSOLE_OUTPUT.value = "".join((CONSOLE_OUTPUT.value, content, "\n"))
    CONSOLE_OUTPUT.scrollTop = CONSOLE_OUTPUT.scrollHeight


def clear_console_output(*_):
    """Clears the console output"""
    CONSOLE_OUTPUT.value = ""


async def evaluate_python(*_):
    """Evaluates code form the code input and writes to console output."""
    toggle_inputs(True)
    code = CODE.value
    add_code_to_console_output(code)
    try:
        content = await pyodide.eval_code_async(code, globals=globals())
        if content is not None:
            print_to_console_output(content)
    except Exception as exception:  # pylint: disable=broad-except
        print_to_console_output(exception)
    toggle_inputs(False)


async def create_client(*_):
    """Create a `TextAnalytics` and a `FormRecognizer` clients in the global Python
    scope with the `PyodideTransport` transport.
    """
    try:
        key = KEY_INPUT.value
        endpoint = ENDPOINT_INPUT.value
        client_type = CLIENT_TYPE_SELECT.value

        global client  # pylint: disable=invalid-name, global-statement
        if client_type == "text-analytics":
            client = TextAnalyticsClient(
                endpoint=endpoint,
                credential=AzureKeyCredential(key),
                transport=PyodideTransport(),  # pylint: disable=undefined-variable
            )
            print_to_console_output("TextAnalytics client created successfully!")
        elif client_type == "form-recognizer":
            client = FormRecognizerClient(
                endpoint=endpoint,
                credential=AzureKeyCredential(key),
                transport=PyodideTransport(),  # pylint: disable=undefined-variable
            )
            print_to_console_output("FormRecognizer client created successfully!")
        elif client_type == "blob-storage":
            client = BlobServiceClient(
                account_url=endpoint,
                credential=key,
                transport=PyodideTransport(),  # pylint: disable=undefined-variable
            )
            print_to_console_output("BlobService client created successfully!")
        else:
            raise Exception(f"{client_type} is not a valid client type.")
    except Exception as exception:
        print(exception)


def tab_listener(event, tab_size=4):
    """So pressing <Tab> creates four spaces in the code input rather than
    moving into the next element. Inspired by
    https://stackoverflow.com/questions/6637341/use-tab-to-indent-in-textarea
    """
    this = event.currentTarget
    if event.key == "Tab":
        event.preventDefault()
        start = this.selectionStart
        end = this.selectionEnd
        this.value = this.value[:start] + " " * tab_size + this.value[end:]
        this.selectionStart = this.selectionEnd = start + tab_size


def update_example(*_):
    """Put example code into the code input."""
    example_name = EXAMPLE_SELECT.value
    if example_name:
        CODE.value = EXAMPLES[example_name].replace("  # type: ignore", "")


def toggle_docs(*_):
    """Toggle documentation."""
    for element in js.document.getElementsByClassName("docs"):
        if element.style.display != "none":
            element.style.display = "none"
        else:
            element.style.display = "block"


# Add events to DOM elements.
get_element_by_id("code").addEventListener(
    "keydown", pyodide.create_proxy(tab_listener)
)
get_element_by_id("run").onclick = evaluate_python
get_element_by_id("toggle-help").onclick = toggle_docs
get_element_by_id("clear").onclick = clear_console_output
get_element_by_id("upload").onclick = save_files
get_element_by_id("create-client").onclick = create_client
EXAMPLE_SELECT.onchange = update_example
