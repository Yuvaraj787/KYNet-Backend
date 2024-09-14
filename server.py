from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

@app.route('/add_data', methods=['POST'])
def add_data():
    # Get JSON data from request
    data = eval(request.json)

    # Check if data is a list of lists
    if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
        return jsonify({"message": "Invalid data format"}), 400

    # Append data to CSV file
    with open('network_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return jsonify({"message": "Data added successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
