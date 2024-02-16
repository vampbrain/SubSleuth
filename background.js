chrome.runtime.onInstalled.addListener(function () {
    console.log("Subsleuth extension installed or updated.");
  });
  
chrome.action.onClicked.addListener(function (tab) {
  const currentUrl = tab.url;

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const activeTab = tabs[0];
    chrome.tabs.sendMessage(activeTab.id, { message: "checkUrl", url: currentUrl });
  });
});
  
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.message === "result") {
    const result = request.result;

    // Display a notification with the result
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icon.png",
      title: "Subsleuth",
      message: result.isMalicious ? "This website is malicious!" : "This website is safe.",
    });
  }
});
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === 'highlightDealOfTheDay') {
      console.log('Received message from popup script. Forwarding to content script...');
      // Send a message to the content script to highlight "deal of the day"
      
      chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        var activeTab = tabs[0];
      
        // Use chrome.scripting.executeScript instead
        chrome.scripting.executeScript({
          target: { tabId: activeTab.id, allFrames: true },
          files: ['content.js'],
        }).then(() => {
          // Send message only after successful script injection
          chrome.tabs.sendMessage(activeTab.id, { action: 'highlightDealOfTheDay' });
        }).catch(error => {
          // Handle potential errors during script injection
          console.error('Error injecting script:', error);
        });
      });
  }
});