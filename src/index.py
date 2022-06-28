# pyright: reportMissingImports=false, reportUndefinedVariable=false
# pylint: disable=import-error
import js
import pyodide
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

get_element_by_id = js.document.getElementById
USER_INPUT_CLASS_NAME = "user-input"
CONSOLE_OUTPUT = get_element_by_id("output")
CONSOLE_INPUT = get_element_by_id("code")
KEY_INPUT = get_element_by_id("key")
ENDPOINT_INPUT = get_element_by_id("endpoint")
FILE_UPLOAD = get_element_by_id("file-upload")

client = None  # pylint: disable=invalid-name


def read_file_async(file):
    """Return a promise that resolves to the contents of a file.
    See:
    https://stackoverflow.com/questions/34495796/javascript-promises-with-filereader"""

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
        print_to_console_output(f"Added {file.name}")
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
    code = CONSOLE_INPUT.value
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
    key = KEY_INPUT.value
    endpoint = ENDPOINT_INPUT.value

    global client  # pylint: disable=invalid-name, global-statement
    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        transport=PyodideTransport(),  # pylint: disable=undefined-variable
    )


def tab_listener(event, tab_size=4):
    """So pressing <Tab> creates four spaces. Inspired by
    https://stackoverflow.com/questions/6637341/use-tab-to-indent-in-textarea"""
    this = event.currentTarget
    if event.key == "Tab":
        event.preventDefault()
        start = this.selectionStart
        end = this.selectionEnd
        this.value = this.value[0:start] + " " * tab_size + this.value[end:]
        this.selectionStart = this.selectionEnd = start + tab_size


# Add events to DOM elements.
get_element_by_id("code").addEventListener(
    "keydown", pyodide.create_proxy(tab_listener)
)
get_element_by_id("run").onclick = evaluate_python
get_element_by_id("clear").onclick = clear_console_output
get_element_by_id("upload").onclick = save_files
get_element_by_id("create-client").onclick = create_client
