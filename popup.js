document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('analyseButton').addEventListener('click', function(){
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      var activeTab = tabs[0];
      url_u=activeTab.url
      console.log(url_u);
      sendUrlToServer(url_u);
    });
   
    analyzeLinks();
    highlightKeywords();
  });
  document.getElementById('copyUrlButton').addEventListener('click', copyUrl);
});
function sendUrlToServer(url) {
  fetch('http://localhost:5000/urlget', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: url })
  })
  .then(response => response.json())
  .then(data => {
      console.log('Received response from server:', data);
      // Print the two values received from the server
      console.log('Result 1:', data.result1);
      console.log('Result 2:', data.result2);
      if (data.result2 === 'Misleading labeling') {
        document.getElementById('result').innerText = data.result2;
        document.getElementById('desc').innerHTML="A misleading label is false or deceptive information on a product, leading consumers to misunderstand its qualities or attributes.";
        document.getElementById("result2").innerText='Most Frequent Sentiment Label: '+ data.result1;
      } 
      else {
        document.getElementById('result').innerText = 'Request failed!';
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}


function copyUrl() {
  var url_u;
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var activeTab = tabs[0];
    url_u=activeTab.url
    console.log(url_u);
    
  });
  return url_u;
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
function highlightKeywords() {
  var keywords = ["limited time offer", "act now", "hurry up", "limited offer", "deal of the day", "time-limited", "last chance", "up to", "off", "upto"];
  var bodyText = document.body.innerHTML;
  for (var i = 0; i < keywords.length; i++) {
    var keywordRegex = new RegExp("\\b(" + keywords[i] + ")\\b", "gi");
    var matches = bodyText.match(keywords);
    if (matches) {
      for (var j = 0; j < matches.length; j++) {
        var keyword = matches[j];
        var span = document.createElement("span");
        span.style.backgroundColor = "yellow";
        span.style.padding = "2px";
        span.textContent = keyword;
        var range = document.createRange();
        range.selectNode(document.body.querySelector("*").contains(matches[j]));
        range.surroundContents(span);
      }
    }
  }
}