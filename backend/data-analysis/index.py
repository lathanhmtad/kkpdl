import requests
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import pandas as pd

app = Flask(__name__)
CORS(app)

DATABASE_API = 'http://localhost:5000/db-api'

@app.route('/api/team-history', methods=['GET'])
def get_team_history():
    # Kết nối MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="football_db"
    )
    # Truy vấn dữ liệu
    query = """
    SELECT match_date, goals_home, yellow_cards_home, red_cards_home, corner_home
    FROM team_history
    WHERE team_id = 33 AND match_date >= '2024-07-01'
    ORDER BY match_date ASC;
    """
    df = pd.read_sql(query, connection)
    connection.close()

    # Chuyển đổi dữ liệu thành danh sách JSON
    data = df.to_dict(orient='records')
    return jsonify(data)

@app.route('/api/teams', methods=['GET'])
def get_teams():
    teams = requests.get(f'{DATABASE_API}/teams').json().get('data', [])
    return jsonify({'teams': teams}), 200

@app.route('/api/trend/<int:team_id>', methods=['GET'])
def trend(team_id):
    team_history = requests.get(f'{DATABASE_API}/trend/{team_id}').json().get('data', [])
    return jsonify(team_history)

@app.route('/api/seasonal/<int:team_id>', methods=['GET'])
def seasonal(team_id):
    return jsonify(requests.get(f'{DATABASE_API}/seasonal/{team_id}').json())

@app.route('/api/weekly/<int:team_id>', methods=['GET'])
def get_weekly_stats(team_id):
    return jsonify(requests.get(f'{DATABASE_API}/weekly-stats/{team_id}').json())

@app.route('/api/daily/<int:team_id>', methods=['GET'])
def get_daily_stats(team_id):
    return jsonify(requests.get(f'{DATABASE_API}/daily-stats/{team_id}').json())

@app.route('/api/monthly/<int:team_id>', methods=['GET'])
def get_monthly_stats(team_id):
    return jsonify(requests.get(f'{DATABASE_API}/monthly-stats/{team_id}').json())

@app.route('/api/correlation', methods=['GET'])
def correlation():
    return jsonify(requests.get(f'{DATABASE_API}/correlation').json())

@app.route('/api/spider/<int:home>/<int:away>', methods=['GET'])
def spider(home, away):
    return jsonify(requests.get(f'{DATABASE_API}/spider-chart/{home}/{away}').json())

@app.route('/api/predict/<int:home>/<int:away>', methods=['GET'])
def predict(home, away):
    return jsonify(requests.get(f'{DATABASE_API}/predict/{home}/{away}').json())

@app.route('/api/rank/<int:team_id>', methods=['GET'])
def rank(team_id):
    return jsonify(requests.get(f'{DATABASE_API}/rank/{team_id}').json())
    
if __name__ == '__main__':
    app.run(debug=True, port=5001, host='localhost')