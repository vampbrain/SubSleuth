from flask import Flask, request, jsonify
from nlp import urlget

app = Flask(__name__)

@app.route('/urlget', methods=['POST'])
def get_url():
    data = request.get_json()
    url = data.get('url', '')

    # Call the urlget function with the received URL
    result1, result2 = urlget(url)
    
    return jsonify({'result1': result1, 'result2': result2})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
