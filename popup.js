document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('analyzeButton').addEventListener('click', analyzeLinks);
  document.getElementById('copyUrlButton').addEventListener('click', copyUrl);
});



function copyUrl() {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var activeTab = tabs[0];
    console.log(activeTab.url);
  });
}

//function analyzeLinks() {
//  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
//    var activeTab = tabs[0];
//    chrome.tabs.sendMessage(activeTab.id, { action: 'analyzeLinks' });
//  });
//}

chrome.runtime.onMessage.addListener(
  function (request, sender, sendResponse) {
    if (request.action === 'displayResult') {
      document.getElementById('result').innerText = request.result;
    }
  }
);
function analyzeLinks() {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      var activeTab = tabs[0];
      chrome.scripting.executeScript({
          target: { tabId: activeTab.id },
          files: ['content.js']
      }).then(() => {
          // Script injected, now send a message to collect links
          chrome.tabs.sendMessage(activeTab.id, { action: 'collectLinks' }, function (response) {
              // Handle response containing links
              if (response && response.links) {
                  console.log('Links:', response.links);
                  // You can further process the links here
              }
          });
      }).catch(err => {
          console.error('Failed to inject script:', err);
      });
  });
}