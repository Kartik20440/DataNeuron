import json
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

data_file = "data.json"
count_file = "count.json"

def load_data():
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f)

def load_count():
    try:
        with open(count_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"add": 0, "update": 0}

def save_count(count):
    with open(count_file, "w") as f:
        json.dump(count, f)

@app.route("/add", methods=["POST"])
def add_data():
    try:
            
        data = request.json
        print(data)
        save_data([data])
        # Update count for "add" operation
        count = load_count()
        count["add"] += 1
        save_count(count)
        return "Data added successfully."
    # catch error
    except Exception as e:
        print("this is error ",e)
    

@app.route("/update", methods=["PUT"])
def update_data():
    data = request.json
    existing_data = load_data()
    # esisting_data = list(existing_data.values())
    existing_data.append(data)
    save_data(existing_data)
    # Update count for "update" operation
    count = load_count()
    count["update"] += 1
    save_count(count)
    return "Data updated successfully."

@app.route("/count", methods=["GET"])
def get_count():
    count = load_count()
    return jsonify(count)

if __name__ == "__main__":
    # create file if dont exist "data.json" && "count.json" using os
    if not os.path.exists("data_file"):
        save_data([])
    if not os.path.exists("count_file"):
        save_count({"add": 0, "update": 0})
    app.run(debug=True)
