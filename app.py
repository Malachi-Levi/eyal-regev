from flask import Flask, jsonify, request, send_file 
from flask_cors import CORS
import os
import random
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))


@app.route('/retiringDate', methods=['GET'])
def get_retiringDate():
    current_date = datetime.now()
    future_date = datetime.strptime('25/12/2032', '%d/%m/%Y')
    
    # Calculate the difference in hours
    time_difference = future_date - current_date
    hours_until = time_difference.total_seconds() / 3600
    minutes_until = time_difference.total_seconds() / 60
    
    return jsonify({"hoursUntilRetirement": hours_until,"minutesUntilRetirement": minutes_until, "future_date": future_date})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
