chrome.runtime.onInstalled.addListener(function () {
    console.log("Subsleuth extension installed or updated.");
});

chrome.browserAction.onClicked.addListener(function (tab) {
    const currentUrl = tab.url;

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const activeTab = tabs[0];
        fetch('http://localhost:5000/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: currentUrl }),
        })
            .then(response => response.json())
            .then(data => {
                // Handle the response, e.g., display malicious links in the popup
                console.log(data);
                chrome.notifications.create({
                    type: "basic",
                    iconUrl: "icon.png",
                    title: "Subsleuth",
                    message: `Malicious Links: ${data.malicious_links.join(', ')}`,
                });
            })
            .catch(error => console.error('Error:', error));
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
