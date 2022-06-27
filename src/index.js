import initPy from './init.py';
import transportPy from './transport.py';
import createClientPy from './create_client.py';
import getExamples from './examples.js';

const output = document.getElementById('output');
output.value = 'Initializing...\n';
const code = document.getElementById('code');

const select = document.getElementById('example');
const run = document.getElementById('run');
const clear = document.getElementById('clear');
const file_upload = document.getElementById('file-upload');
const upload = document.getElementById('upload');
const buttons = document.getElementsByClassName('user-input');
const EXAMPLES = getExamples();

/**
 * Read the bytes of a file. See
 * https://stackoverflow.com/questions/34495796/javascript-promises-with-filereader
 */
function readFileAsync(file) {
  return new Promise((resolve, reject) => {
    let reader = new FileReader();

    reader.onload = () => {
      resolve(reader.result);
    };

    reader.onerror = reject;

    reader.readAsArrayBuffer(file);
  });
}

async function createClient() {
  const pyodide = await pyodideReadyPromise;
  const key = document.getElementById('key').value;
  const endpoint = document.getElementById('endpoint').value;
  const client = document.getElementById('client').value;
  let py = `client = ${client}(endpoint="${endpoint}", credential=AzureKeyCredential("${key}"), transport=PyodideTransport())`;
  console.log(py);
  await pyodide.runPythonAsync(py);
}
/**
 * Initialize python environment and create the client
 */
async function init(pyodide) {
  pyodide.registerJsModule('js_file', { readFileAsync });
  await pyodide.loadPackage('micropip');
  await pyodide.runPythonAsync(initPy);
  await pyodide.globals.get('load_packages')();
  await pyodide.runPythonAsync(transportPy);
  await pyodide.runPythonAsync(createClientPy);
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

function addCodeToOutput(code) {
  let consoleCode = code.trim().split('\n').join('\n... ');
  output.value += '>>> ' + consoleCode + '\n';
}

/**
 * Add formatted multi-line code to the output.
 */
function addToOutput(s) {
  if (typeof s !== 'undefined') {
    output.value += s + '\n';
  }

  // Scrolls the output to the bottom.
  output.scrollTop = output.scrollHeight;
}

/**
 * Clears the output box.
 */
function clearConsole() {
  output.value = '';
}

async function main() {
  let pyodide = await loadPyodide({
    stdout: (x) => (output.value += x + '\n'),
    stderr: (x) => (output.value += x + '\n'),
  });
  await init(pyodide);
  enableButtons();
  output.value += 'Ready!\n';
  upload.onclick = pyodide.globals.get('save_files');

  return pyodide;
}

const pyodideReadyPromise = main();
window.pyodideReadyPromise = pyodideReadyPromise;

async function evaluatePython() {
  disableButtons();
  let pyodide = await pyodideReadyPromise;
  try {
    addCodeToOutput(code.value);
    const output = await pyodide.runPythonAsync(code.value);
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

window.addToOutput = addToOutput;
window.updateExample = updateExample;
window.evaluatePython = evaluatePython;
window.clearConsole = clearConsole;
window.createClient = createClient;

// See https://stackoverflow.com/questions/6637341/use-tab-to-indent-in-textarea
document.getElementById('code').addEventListener('keydown', function (e) {
  if (e.key == 'Tab') {
    e.preventDefault();
    var start = this.selectionStart;
    var end = this.selectionEnd;

    // set textarea value to: text before caret + tab + text after caret
    this.value =
      this.value.substring(0, start) + '    ' + this.value.substring(end);

    // put caret at right position again
    this.selectionStart = this.selectionEnd = start + 4;
  }
});
