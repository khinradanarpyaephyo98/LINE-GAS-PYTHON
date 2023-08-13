from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/endpoint', methods=['GET'])
def api_endpoint():
    # Process the request and call the actual API
    # Return the response to Google Apps Script
    response_data = {"message": "Hello from Python API"}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run()
