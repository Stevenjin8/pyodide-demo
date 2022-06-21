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
const buttons = [select, run, clear, file_upload];
const EXAMPLES = getExamples();

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
  await pyodide.runPythonAsync(
    `textanalytics_client, formrecognizer_client = await create_clients()`,
  );
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
  let consoleCode = code.value.trim().split('\n').join('\n... ');
  output.value += '>>> ' + consoleCode + '\n';
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
  let pyodide = await loadPyodide();
  await init(pyodide);
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

window.updateExample = updateExample;
window.evaluatePython = evaluatePython;
window.clearConsole = clearConsole;
