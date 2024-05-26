from flask import Flask, request
import json
import numpy as np
import joblib

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the prediction API. Use /predict to get predictions."

@app.route('/predict', methods=['GET'])
def predict():
    # stub input features
    request_json = request.get_json()
    x = request_json['input']
    #print(x)
    x_in = np.array(x).reshape(1, -1)
    # load model
    loaded_rf = joblib.load("/Users/tunakisaaga/Desktop/ds_salary_proj-master/random_forest.joblib")
    prediction = loaded_rf.predict(x_in)[0]
    response = json.dumps({'response': prediction})
    return response, 200

if __name__ == '__main__':
    app.run(debug=True)