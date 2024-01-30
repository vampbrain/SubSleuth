# web_app.py
from flask import Flask, request, jsonify
from model import classify_links, extract_links

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_url():
    data = request.get_json()
    url = data.get('url', '')

    if not url:
        return jsonify({'error': 'Invalid request'}), 400

    links = extract_links(url)
    malicious_links, subscription_links = classify_links(links)

    result = {
        'url': url,
        'malicious_links': malicious_links,
        'subscription_links': subscription_links
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
