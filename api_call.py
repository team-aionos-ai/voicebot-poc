from flask import Flask, request, jsonify

app = Flask(__name__)

# Global storage for step data
step_data = {
            'step_number':'1',
            "description": 'No description provided.',
            "command": 'N/A',
            "additional_info":  'N/A'
        }

# Global storage for transcript data
transcript_data = {
            'transcript':'N/A',
            "context": 'N/A',
        }

@app.route('/health', methods=['GET'])
def health_check():
    """
    GET request to check server health
    """
    return jsonify({"status": "Server is healthy!"}), 200

@app.route('/receive_step_details', methods=['POST'])
def receive_step_details():
    """
    POST request to receive step details
    """
    try:
        # Parse JSON data from the request
        data = request.get_json()
        
        global step_data
        step_data = {
            'step_number': data.get('step_number', '1'),
            "description": data.get('description', 'No description provided.'),
            "command": data.get('command', 'N/A'),
            "additional_info": data.get('additional_info', 'N/A').replace('\n', '<br>')
        }
        print(data)
        
        return jsonify({"status": "success", "message": "Step details received."}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_step_details', methods=['GET'])
def get_step_details():
    """
    GET request to fetch the latest step details
    """
    try:
        if not step_data:
            return jsonify({"error": "No step details available."}), 404
        
        return jsonify(step_data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset_step_details', methods=['POST'])
def reset_step_details():
    """
    POST request to reset the step details to default
    """
    global step_data
    step_data = {
        'step_number': '0',
        "description": '',
        "command": '',
        "additional_info": ''
    }
    return jsonify({"status": "success", "message": "Step details reset to default."}), 200

@app.route('/receive_transcript', methods=['POST'])
def receive_transcript():
    """
    POST request to receive step details
    """
    try:
        # Parse JSON data from the request
        data = request.get_json()
        
        global transcript_data
        transcript_data = {
            'transcript': data.get('transcript', 'N/A'),
            "context": data.get('context', 'N/A'),
        }
        print(data)
        
        return jsonify({"status": "success", "message": "Transcript received."}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    """
    GET request to fetch the latest step details
    """
    try:
        if not transcript_data:
            return jsonify({"error": "No transcript available."}), 404
        
        return jsonify(transcript_data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset_transcript', methods=['POST'])
def reset_transcript():
    """
    POST request to reset the step details to default
    """
    global transcript_data
    transcript_data = {
        'transcript':'N/A',
            "context": 'N/A'
    }
    return jsonify({"status": "success", "message": "Step details reset to default."}), 200


if __name__ == '__main__':
    app.run(host='172.31.3.215', port= 8502)
