from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

@app.route('/add_data', methods=['POST'])
def add_data():
    # Get JSON data from request
    print("Request came");
    print(request.json);
    data = request.json['data'];

    # Check if data is a list of lists
    if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
        return jsonify({"message": "Invalid data format"}), 400

    # Append data to CSV file
    with open('updated_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("write success full");

    return jsonify({"message": "Data added successfully"}), 200

@app.route('/data/network_data.csv', methods=['GET'])
def send_data_file():
    return send_file("./network_data.csv", as_attachment=True);

@app.route('/data/updated_data.csv', methods=['GET'])
def send_file2():
    return send_file("./updated_data.csv", as_attachment=True);

if __name__ == '__main__':
    app.run(debug=False, port=80, host="0.0.0.0")
