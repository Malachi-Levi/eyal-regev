from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import logging
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)

# MongoDB Atlas connection details
MONGO_URI = "mongodb+srv://Eyal:1234@cluster0.hwltrqz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)

# Specify the database and collection
db = client['EyalRegev']
collection = db['EyalWeight']

# Password for protected routes
PASSWORD = '1'

@app.route('/retiringDate', methods=['GET'])
def get_retiringDate():
    current_date = datetime.now()
    future_date = datetime.strptime('25/12/2032', '%d/%m/%Y')
    
    # Calculate the difference in hours
    time_difference = future_date - current_date
    hours_until = time_difference.total_seconds() / 3600
    minutes_until = time_difference.total_seconds() / 60
    
    return jsonify({"hoursUntilRetirement": hours_until,"minutesUntilRetirement": minutes_until, "future_date": future_date})

@app.route('/getData', methods=['GET'])
def get_getData():
    try:
        print("This is a message printed to the console")
        # Fetch data from MongoDB collection
        data = list(collection.find({}, {"_id": 0}))  # Exclude the _id field from the result
        print("This is a message printed to the console")
        return jsonify({"dbData": data})
    except Exception as e:
        logging.error(f"Error fetching data from MongoDB: {e}")
        return jsonify({"error": "Failed to fetch data"}), 500

@app.route('/writeData', methods=['POST'])
def write_data():
    print("This is a message printed to the console")
    try:
        # Get JSON data from the request
        data = request.json
        password = data.pop('password', None)
        
        if not password or password != PASSWORD:
            return jsonify({"error": "Invalid password"}), 403
        
        # Insert data into MongoDB collection
        collection.insert_one(data)
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        logging.error(f"Error writing data to MongoDB: {e}")
        return jsonify({"error": "Failed to insert data"}), 500
    

@app.route('/deleteData', methods=['DELETE'])
def delete_data():
    print("This is a message printed to the console")
    try:
        # Get JSON data from the request
        data = request.json
        print(f"Received data: {data}")
        password = data.pop('password', None)
        print(f"Received password: {password}")
        
        if not password or password != PASSWORD:
            return jsonify({"error": "Invalid password"}), 403
        
        # Delete data from MongoDB collection
        result = collection.delete_one(data)
        if result.deleted_count == 0:
            return jsonify({"error": "No document matched the provided criteria"}), 404
        return jsonify({"message": "Data deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting data from MongoDB: {e}")
        return jsonify({"error": "Failed to delete data"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8080)
