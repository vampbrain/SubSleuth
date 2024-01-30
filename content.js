chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
      if (request.action === 'analyzeLinks') {
        var links = Array.from(document.querySelectorAll('a')).map(a => a.href);
        chrome.runtime.sendMessage({ action: 'displayResult', result: JSON.stringify(links) });
      }
    }
  );
  