chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
      if (request.action === 'analyzeLinks') {
        var links = Array.from(document.querySelectorAll('a')).map(a => a.href);
        chrome.runtime.sendMessage({ action: 'displayResult', result: JSON.stringify(links) });
      }
    }
  );
// Function to collect links on the page
function collectLinks() {
  const links = Array.from(document.querySelectorAll('a[href]')).map(a => a.href);
  return links;
}

// Listen for messages from the extension
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'collectLinks') {
      const links = collectLinks();
      // Send the collected links back to the extension
      sendResponse({ links: links });
  }
});
