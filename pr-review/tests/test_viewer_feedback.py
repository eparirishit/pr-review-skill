"""Execute the generated viewer's real handlers with an in-memory HTTP boundary."""
from pathlib import Path
import shutil
import subprocess
import unittest


@unittest.skipUnless(shutil.which("node"), "Node unavailable; viewer JavaScript check not run")
class ViewerFeedbackTests(unittest.TestCase):
    def test_save_and_submit_handle_http_errors(self):
        viewer = Path(__file__).resolve().parents[2] / "evaluation/review.html"
        script = r"""
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(process.argv[1], 'utf8');
const start = html.indexOf('    function saveCurrentFeedback()');
const end = html.indexOf('    function closeDoneDialog()', start);
assert(start >= 0 && end > start);
(async () => {
  for (const response of ['success', 'http-error', 'network-error']) {
    let downloaded = 0, visible = false;
    const fields = {
      feedback: {value: 'Keep this feedback'},
      'feedback-status': {textContent: ''},
      'done-overlay': {classList: {add() {visible = true;}}},
    };
    const context = vm.createContext({
      EMBEDDED_DATA: {runs: [{id: 'one'}]}, currentIndex: 0, feedbackMap: {},
      document: {
        getElementById(id) {return fields[id];},
        createElement() {return {click() {downloaded++;}};},
      },
      fetch: async () => {
        if (response === 'network-error') throw Error('offline');
        return {ok: response === 'success', status: response === 'success' ? 200 : 405};
      },
      Blob, URL: {createObjectURL() {return 'blob:test';}, revokeObjectURL() {}},
    });
    vm.runInContext(html.slice(start, end), context);
    vm.runInContext('saveCurrentFeedback(); showDoneDialog();', context);
    await new Promise(resolve => setImmediate(resolve));
    assert.equal(fields['feedback-status'].textContent,
      response === 'success' ? 'Saved' : 'Will download on submit', response);
    assert.equal(downloaded, response === 'success' ? 0 : 1, response);
    assert.equal(visible, true, response);
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        result = subprocess.run(["node", "-e", script, str(viewer)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
