import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins="*")  # Enable CORS for all origins

# File paths for storing data and count
data_file = "data.json"
count_file = "count.json"

# Function to load data from JSON file
def load_data():
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Function to save data to JSON file
def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f)

# Function to load count from JSON file
def load_count():
    try:
        with open(count_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"add": 0, "update": 0}

# Function to save count to JSON file
def save_count(count):
    with open(count_file, "w") as f:
        json.dump(count, f)

# Endpoint to add data via POST request
@app.route("/add", methods=["POST"])
def add_data():
    try:
        data = request.json
        save_data([data])  # Save new data
        # Update count for "add" operation
        count = load_count()
        count["add"] += 1
        save_count(count)
        return "Data added successfully."
    except Exception as e:
        print("Error:", e)

# Endpoint to update data via PUT request
@app.route("/update", methods=["PUT"])
def update_data():
    data = request.json
    existing_data = load_data()
    existing_data.append(data)  # Append new data to existing
    save_data(existing_data)  # Save updated data
    # Update count for "update" operation
    count = load_count()
    count["update"] += 1
    save_count(count)
    return "Data updated successfully."

# Endpoint to get count of add and update operations
@app.route("/count", methods=["GET"])
def get_count():
    count = load_count()
    return jsonify(count)

if __name__ == "__main__":
    # Create files if they don't exist: "data.json" & "count.json" using os
    if not os.path.exists(data_file):
        save_data([])  # Initialize with empty list
    if not os.path.exists(count_file):
        save_count({"add": 0, "update": 0})  # Initialize counts
    app.run(host='0.0.0.0', port='10000', debug=True)  # Run Flask app on specified host and port
