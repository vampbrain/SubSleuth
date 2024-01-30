# SubSleuth Chrome Extension

## Overview
SubSleuth is a Chrome extension designed to analyze web links on a page, identifying potentially malicious links and subscription/unsubscription links. This work is currently in progress

## Features
- **Link Analysis:** Analyze links on the current webpage for malicious content.
- **Subscription Links:** Identify links related to subscriptions/unsubscriptions.

## How It Works
1. The extension utilizes a background script (`background.js`) and a content script (`content.js`) to interact with the browser.
2. Clicking on the extension icon triggers the analysis of links on the current webpage.
3. Malicious links and subscription links are identified using a machine learning model in the `scanner.py` backend.

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Machine Learning:** Scikit-learn, XGBoost
- **Web Scraping:** BeautifulSoup
- **Chrome Extension APIs:** `chrome.runtime`, `chrome.tabs`, `chrome.notifications`

## Installation
1. Clone the repository: `git clone https://github.com/vampbrain/SubSleuth.git`
2. Load the extension in Chrome by navigating to `chrome://extensions/`, enabling "Developer mode," and selecting "Load unpacked."

## Usage
1. Click on the SubSleuth extension icon in the Chrome toolbar.
2. Press the "Analyze Links" button to initiate link analysis.
3. Malicious links and subscription links will be displayed in the extension popup.

## Known Issues
- Service worker registration might fail due to restrictions on some websites.

## Contributing
Contributions are welcome! Please submit bug reports or feature requests via GitHub issues.

## License
This project is licensed under the [MIT License](LICENSE).

Happy sleuthing!
