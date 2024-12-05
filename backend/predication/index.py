import requests
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import pandas as pd

app = Flask(__name__)
CORS(app)

DATABASE_API = 'http://localhost:5000/db-api'

@app.route('/api/predict/<int:home>/<int:away>', methods=['GET'])
def predict(home, away):
    return jsonify(requests.get(f'{DATABASE_API}/predict/{home}/{away}').json())

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='localhost')
