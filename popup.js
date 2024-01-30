document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('analyzeButton').addEventListener('click', analyzeLinks);
  document.getElementById('copyUrlButton').addEventListener('click', copyUrl); // Adding event listener for the copyUrl function
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
function scanUrl(url) {
  // Define the URL of your Flask API endpoint
  const apiUrl = 'http://localhost:5000/scan';

  // Define the request body containing the URL to scan
  const requestBody = {
      url: url
  };

  // Make a POST request to the Flask API endpoint
  fetch(apiUrl, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
  })
  .then(response => {
      // Check if the response was successful (status code 200)
      if (response.ok) {
          // Parse the JSON response
          return response.json();
      } else {
          // Handle errors
          throw new Error('Failed to scan URL: ' + response.statusText);
      }
  })
  .then(data => {
      // Process the response data
      console.log('Malicious Links:', data.malicious_links);
  })
  .catch(error => {
      // Handle errors
      console.error('Error scanning URL:', error);
  });
}

// Example usage: call the scanUrl function with a URL to scan
const urlToScan = 'https://example.com';
scanUrl(urlToScan);
