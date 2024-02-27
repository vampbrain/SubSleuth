
console.log('testing...');

// Function to collect links on the page
function collectLinks() {
  const links = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
  return links;
}

// Listen for messages from the extension
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'collectLinks') {
      console.log("received the collect links");
      const links = collectLinks();
      // Send the collected links back to the extension
      sendResponse({ links: links });
  }
});
// Function to traverse the DOM and highlight keywords
function highlightKeywordsInDom() {
  // List of keywords to search for
  var keywords = ["limited time offer","Deal of the day", "act now", "hurry up", "limited offer", "deal of the day", "time-limited", "last chance", "up to", "off", "upto"];

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
                      boundingBox.style.left = parentElement.offsetLeft + '5px';
                      boundingBox.style.top = parentElement.offsetTop + '5px';
                      boundingBox.style.width = parentElement.offsetWidth + '5px';
                      boundingBox.style.height = parentElement.offsetHeight + '5px';
                      document.body.appendChild(boundingBox);
                  });
              }
          });
      } else if (node.nodeType === Node.ELEMENT_NODE && node.nodeName !== 'SCRIPT' && node.nodeName !== 'STYLE') {
          // Recursively traverse child nodes
          node.childNodes.forEach(traverse);
      }
  }

  // Start traversal from the document body
  traverse(document.body);
}


// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === 'highlightKeywords') {
      console.log("received");
      // Highlight keywords in the DOM
      highlightKeywordsInDom();
  }
});
// Function to highlight "Deal of the day"
// Function to highlight "Deal of the day"
// Function to highlight "deal of the day"
function highlightDealOfTheDay() {
  var keywords = ["Deal of the Day"];

  keywords.forEach(keyword => {
      console.log("Searching for keyword:", keyword);
      var elements = document.querySelectorAll('*');
      elements.forEach(element => {
          var text = element.textContent;
          var index = text.indexOf(keyword);
          while (index !== -1) {
              console.log("Found element with keyword:", element);
              // Wrap each occurrence of the keyword in a <span> element and apply background color
              var before = text.substring(0, index);
              var after = text.substring(index + keyword.length);
              var highlightedText = document.createElement('span');
              highlightedText.textContent = keyword;
              highlightedText.style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
              var container = document.createElement('span');
              container.textContent = before;
              container.appendChild(highlightedText);
              container.appendChild(document.createTextNode(after));
              element.innerHTML = '';
              element.appendChild(container);
              // Continue searching for next occurrence
              text = after;
              index = text.indexOf(keyword);
          }
      });
  });
}

// Trigger the function


// Message listener to trigger the function
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === 'highlightDealOfTheDay') {
      console.log('Received message to highlight "deal of the day"');
      // Highlight "deal of the day" in the active tab
      highlightDealOfTheDay();
  }
});
// content.js

// Function to intercept link clicks

