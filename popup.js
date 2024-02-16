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
    console.log('Button clicked. Sending message to content script...');
    console.log('Button clicked. Sending message to background script...');
    // Send a message to the background script to trigger content script
    chrome.runtime.sendMessage({ action: 'highlightDealOfTheDay' });
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
        var line1 = document.createElement('div');
        var line2 = document.createElement('div');
        var line3 = document.createElement('div');

        // Set text content for each line
        line1.textContent = 'Dark Patten Detected: '+data.result2;
        line2.textContent = "A misleading label is false or deceptive information on a product, leading consumers to misunderstand its qualities or attributes.";
        line3.textContent = 'Most Frequent Sentiment Label: '+ data.result1;

        // Apply Inter font to all lines
        var interFont = 'Inter, sans-serif';
        line1.style.fontFamily = interFont;
        line2.style.fontFamily = interFont;
        line3.style.fontFamily = interFont;

        // Apply bold font weight to the first line
        line1.style.fontWeight = 'bold';

        // Set marginBottom for each line to create padding
        line1.style.marginTop='15px';
        line1.style.marginBottom = '10px'; // Adjust the value as needed
        line2.style.marginBottom = '10px'; // Adjust the value as needed
        line3.style.marginBottom = '15px'; // Adjust the value as needed

        // Get the container element where you want to append the lines
        var container = document.getElementById('content'); // Replace 'container' with the actual ID of your container

        // Append the lines to the container
        container.appendChild(line1);
        container.appendChild(line2);
        container.appendChild(line3);
        // Create buttons
        var redButton = document.createElement('button');
        redButton.textContent = 'Go Back'; // Set text for the first button
        redButton.style.backgroundColor = '#E51A1A'; // Use the specified color code
        redButton.style.color = 'white';
        redButton.style.borderRadius = '8px';
        redButton.style.marginRight = '10px';
        redButton.style.padding = '8px 20px'; // Add padding to the button
        redButton.style.fontSize = '13px';  // Add curvature to the button
        redButton.style.fontFamily = 'Inter, sans-serif'; // Use Inter font
        redButton.style.fontWeight = 'bold';
        var blackButton = document.createElement('button');
        blackButton.textContent = 'Proceed Anyway'; // Set text for the second button
        blackButton.style.backgroundColor = '#472424'; // Use the specified color code
        blackButton.style.color = 'white';
        blackButton.style.borderRadius = '8px'; // Add curvature to the button
        blackButton.style.padding = '8px 20px'; // Add padding to the button
        blackButton.style.fontSize = '13px'; // Increase font size
        blackButton.style.fontFamily = 'Inter, sans-serif'; // Use Inter font
        blackButton.style.fontWeight = 'bold';
        // Create container
        var buttonContainer = document.getElementById('buttonContainer');

        // Append buttons to container
        buttonContainer.appendChild(redButton);
        buttonContainer.appendChild(blackButton);

        // Add event listeners
        redButton.addEventListener('click', function() {
            history.back(); // Navigate back when the first button is clicked
        });

        blackButton.addEventListener('click', function() {
            // Close the extension popup when the second button is clicked
            window.close();
        });

      } 
      else if (data.result2 === 'False urgency') {
        // Create three div elements
        var line1 = document.createElement('div');
        var line2 = document.createElement('div');
        var line3 = document.createElement('div');

        // Set text content for each line
        line1.textContent = 'Dark Patten Detected: '+data.result2;
        line2.textContent = "False urgency is a tactic used in marketing or sales to create a sense of imminent need or scarcity, even when it's not genuine. ";
        line3.textContent = 'Most Frequent Sentiment Label: '+ data.result1;

        // Apply Inter font to all lines
        var interFont = 'Inter, sans-serif';
        line1.style.fontFamily = interFont;
        line2.style.fontFamily = interFont;
        line3.style.fontFamily = interFont;

        // Apply bold font weight to the first line
        line1.style.fontWeight = 'bold';

        // Set marginBottom for each line to create padding
        line1.style.marginBottom = '10px'; // Adjust the value as needed
        line2.style.marginBottom = '10px'; // Adjust the value as needed
        line3.style.marginBottom = '10px'; // Adjust the value as needed

        // Get the container element where you want to append the lines
        var container = document.getElementById('container'); // Replace 'container' with the actual ID of your container

        // Append the lines to the container
        container.appendChild(line1);
        container.appendChild(line2);
        container.appendChild(line3);

        var redButton = document.createElement('button');
        redButton.textContent = 'Go Back'; // Set text for the first button
        redButton.style.backgroundColor = '#E51A1A'; // Use the specified color code
        redButton.style.color = 'white';
        redButton.style.borderRadius = '8px';
        redButton.style.marginRight = '10px';
        redButton.style.padding = '8px 20px'; // Add padding to the button
        redButton.style.fontSize = '13px';  // Add curvature to the button
        redButton.style.fontFamily = 'Inter, sans-serif'; // Use Inter font
        redButton.style.fontWeight = 'bold';
        var blackButton = document.createElement('button');
        blackButton.textContent = 'Proceed Anyway'; // Set text for the second button
        blackButton.style.backgroundColor = '#472424'; // Use the specified color code
        blackButton.style.color = 'white';
        blackButton.style.borderRadius = '8px'; // Add curvature to the button
        blackButton.style.padding = '8px 20px'; // Add padding to the button
        blackButton.style.fontSize = '13px'; // Increase font size
        blackButton.style.fontFamily = 'Inter, sans-serif'; // Use Inter font
        blackButton.style.fontWeight = 'bold';
        // Create container
        var buttonContainer = document.getElementById('buttonContainer');

        // Append buttons to container
        buttonContainer.appendChild(redButton);
        buttonContainer.appendChild(blackButton);

        // Add event listeners
        redButton.addEventListener('click', function() {
            history.back(); // Navigate back when the first button is clicked
        });

        blackButton.addEventListener('click', function() {
            // Close the extension popup when the second button is clicked
            window.close();
        });

      }
      else {
        document.getElementById('result').innerText = 'Request failed!';
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}
// Function to highlight keywords in the active tab
function highlightKeywordsInActiveTab() {
  // List of keywords to search for
  var keywords = ["limited time offer", "act now",,"Deal of the day", "hurry up", "limited offer", "deal of the day", "time-limited", "last chance", "up to", "off", "upto"];

  // Function to traverse all text nodes and highlight keywords
  function traverse(node) {
      if (node.nodeType === Node.TEXT_NODE) {
          var textContent = node.nodeValue;
          // Loop through keywords and highlight occurrences
          keywords.forEach(keyword => {
              var regex = new RegExp('\\b' + keyword + '\\b', 'gi');
              var matches = textContent.match(regex);
              if (matches) {
                  // Create a bounding box for each occurrence
                  matches.forEach(match => {
                      var parentElement = node.parentElement;
                      var boundingBox = document.createElement('div');
                      boundingBox.style.border = '2px solid black';
                      boundingBox.style.position = 'absolute';
                      boundingBox.style.left = parentElement.offsetLeft + 'px';
                      boundingBox.style.top = parentElement.offsetTop + 'px';
                      boundingBox.style.width = parentElement.offsetWidth + 'px';
                      boundingBox.style.height = parentElement.offsetHeight + 'px';
                      document.body.appendChild(boundingBox);
                  });
              }
          });
      } else if (node.nodeType === Node.ELEMENT_NODE && node.nodeName !== 'SCRIPT' && node.nodeName !== 'STYLE') {
          // Recursively traverse child nodes
          node.childNodes.forEach(traverse);
      }
  }

  // Get the active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      // Access the content of the active tab
      chrome.tabs.executeScript(tabs[0].id, {
          code: '(' + function() {
              // Start traversal from the document body
              var traverse = function(node) {
                  // The same traversal logic as above
                  // ...
              };
              traverse(document.body);
          } + ')()'
      });
  });
}

// Call the function to highlight keywords in the active tab


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
// popup.js

// Function to show the warning page in the extension popup
function showWarningPage() {
  // Update the popup HTML content to show the warning page
  document.getElementById('warningPage').style.display = 'block';
}

// Listen for messages from the content script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === 'showWarningPage') {
      // Call the function to show the warning page
      showWarningPage();
  }
});
