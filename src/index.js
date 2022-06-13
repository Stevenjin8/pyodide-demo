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
const buttons = [select, run, clear];
const EXAMPLES = getExamples();

/**
 * Initialize python environment and create the client
 */
async function init(pyodide) {
  await pyodide.loadPackage('micropip');
  await pyodide.runPythonAsync(initPy);
  await pyodide.globals.get('load_packages')();
  await pyodide.runPythonAsync(transportPy);
  await pyodide.runPythonAsync(createClientPy);
  await pyodide.runPythonAsync(`client = await create_client()`);
  updateExample();
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
