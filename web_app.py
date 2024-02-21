from flask import Flask, request, jsonify
from nlp import urlget
from sub import check
from Predicter import predict
app = Flask(__name__)

@app.route('/urlget', methods=['POST'])
def get_url():
    data = request.get_json()
    url = data.get('url', '')

    # Call the urlget function with the received URL
    result1, result2 = urlget(url)
    
    return jsonify({'result1': result1, 'result2': result2})
@app.route('/check', methods=['POST'])
def check_url():
    # Extract URL from the request body
    data = request.get_json()
    url = data.get('url','')

    # Process the URL as needed
    # For example, you can pass it to your existing check() function
    resultsub = check(url)

    # Return the result as JSON
    return jsonify({'result': resultsub})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
