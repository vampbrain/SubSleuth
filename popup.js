
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('analyzeButton').addEventListener('click', analyzeLinks);
});

function analyzeLinks() {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var activeTab = tabs[0];
    chrome.tabs.sendMessage(activeTab.id, { action: 'analyzeLinks' });
  });
}

chrome.runtime.onMessage.addListener(
  function (request, sender, sendResponse) {
    if (request.action === 'displayResult') {
      document.getElementById('result').innerText = request.result;
    }
  }
);
