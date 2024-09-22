
from flask import Flask, request, jsonify
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})   #  This allows all origins

# Replace these with your actual details
USER_ID = "john_doe_17091999"
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"

@app.route('/bfhl', methods=['POST'])
def bfhl_post():
    try:
        data = request.json.get('data', [])
        file_b64 = request.json.get('file_b64', '')

        numbers = [item for item in data if item.isdigit()]
        alphabets = [item for item in data if item.isalpha()]
        highest_lowercase = max((char for char in alphabets if char.islower()), default=None)

        file_valid = False
        file_mime_type = ''
        file_size_kb = 0

        if file_b64:
            try:
                file_data = base64.b64decode(file_b64)
                file_valid = True
                file_size_kb = len(file_data) / 1024
                file_mime_type = guess_mime_type(file_data)
            except:
                file_valid = False

        response = {
            "is_success": True,
            "user_id": USER_ID,
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_alphabet": [highest_lowercase] if highest_lowercase else [],
            "file_valid": file_valid,
            "file_mime_type": file_mime_type,
            "file_size_kb": f"{file_size_kb:.2f}"
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"is_success": False, "error": str(e)}), 400

@app.route('/bfhl', methods=['GET'])
def bfhl_get():
    return jsonify({"operation_code": 1}), 200

def guess_mime_type(file_data):
    if file_data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    elif file_data.startswith(b'\xff\xd8'):
        return 'image/jpeg'
    elif file_data.startswith(b'%PDF'):
        return 'application/pdf'
    else:
        return 'application/octet-stream'

if __name__ == '__main__':
    app.run(host='0.0.0.0')

