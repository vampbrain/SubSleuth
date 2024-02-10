import requests
from bs4 import BeautifulSoup
import joblib
from model2 import main, get_prediction_from_url

# Load the trained model
model_path = "/Users/bharathiraghavan/Downloads/subsleuth/url-model.bin"
model = joblib.load(model_path)

# Define a function to extract links from a webpage
def extract_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        return links
    except Exception as e:
        print(f"Error extracting links: {e}")
        return []

# Define the function to classify links
def classify_links(links):
    malicious_links = []
    for link in links:
        prediction =get_prediction_from_url([link])
        if prediction == 1:
            malicious_links.append(link)
    return malicious_links

# Define the Flask app
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the endpoint for scanning URLs
@app.route('/scan', methods=['POST'])
def scan_url():
    data = request.get_json()
    url = data.get('url', '')

    if not url:
        return jsonify({'error': 'Invalid request'}), 400

    # Extract links from the provided URL
    links = extract_links(url)

    # Classify the extracted links
    malicious_links = classify_links(links)

    # Return the results
    result = {
        'url': url,
        'malicious_links': malicious_links
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
