document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('analyzeButton').addEventListener('click', analyzeLinks);
  document.getElementById('copyUrlButton').addEventListener('click', copyUrl);
});

function analyzeLinks() {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var activeTab = tabs[0];
    chrome.tabs.sendMessage(activeTab.id, { action: 'analyzeLinks' });
  });
}

function copyUrl() {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var activeTab = tabs[0];
    var url = activeTab.url;

    // Retrieve existing URLs from storage
    chrome.storage.local.get({ urls: [] }, function (data) {
      var urls = data.urls;

      // Add the current URL to the list
      urls.push(url);

      // Save the updated list back to storage
      chrome.storage.local.set({ urls: urls }, function () {
        console.log('URL added:', url);
        // Notify the background script to update the badge
        chrome.runtime.sendMessage({ message: 'updateBadge' });
      });
    });
  });
}

chrome.runtime.onMessage.addListener(
  function (request, sender, sendResponse) {
    if (request.action === 'displayResult') {
      document.getElementById('result').innerText = request.result;
    }
  }
);
