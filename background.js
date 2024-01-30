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
  