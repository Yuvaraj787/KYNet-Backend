from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import csv
import pandas as pd
import pickle

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

with open('models.pkl', 'rb') as f:
    models = pickle.load(f)


@app.route("/check", methods=["GET", "POST"])
def send():
    return jsonify({message:"Working"})

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json

    if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
        return jsonify({"message": "Invalid data format"}), 400

    with open('network_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return jsonify({"message": "Data added successfully"}), 200

@app.route('/data/network_data.csv', methods=['GET'])
def send_data_file():
    return send_file("./network_data.csv", as_attachment=True);


@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from request (assuming JSON format)
    input_data = request.json

    # Process input data (replace this with actual preprocessing logic if needed)
    x_new = input_data
    
    # Example prediction
    predictions = {}
    for target, model in models.items():
        prediction = model.predict_one(x_new)
        predictions[target] = prediction

    return jsonify(predictions)

@app.route('/learn', methods=['POST'])
def learn():
    # Get input data and actual target values from request
    input_data = request.json['data']
    actual_targets = request.json['targets']  # should include actual 'download_speed', 'upload_speed', 'latency', etc.

    # Process input data (replace this with actual preprocessing logic if needed)
    x_new = input_data
    
    # Incrementally learn for each target variable
    for target, actual_value in actual_targets.items():
        if target in models:
            models[target].learn_one(x_new, actual_value)

    # Optionally, you can save the updated model to persist learning across sessions
    with open('models.pkl', 'wb') as f:
        pickle.dump(models, f)

    return jsonify({"message": "Model updated with new data!"})


@app.route('/tempo_spatial_data', methods=['GET'])
def getSpatialData():
    df = pd.read_csv('updated_data.csv')
    df_formatted = df[['time', 'lat', 'long', 'isp', 'connection_type', 'download_speed', 'upload_speed', 'latency', 'lte_rsrp', 'nr_rsrp']]
    df_formatted['rsrp'] = df_formatted['nr_rsrp'].fillna(df_formatted['lte_rsrp'])
    df_formatted = df_formatted.drop(columns=['lte_rsrp', 'nr_rsrp'])
    formated_dict = df_formatted.to_dict(orient='records')
    return jsonify({"tempo_spatial_data": formated_dict})
    

if __name__ == '__main__':
    app.run(debug=True, port=3000)