from flask import Flask, request, jsonify, Blueprint
import mysql.connector
from sklearn.neural_network import MLPRegressor
import pandas as pd
from flask_cors import CORS
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor

app = Flask(__name__)

CORS(app)

api_bp = Blueprint('api', __name__, url_prefix='/db-api/')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE'] = 'football_club_db'

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@api_bp.route('/team-history', methods=['POST'])
def insert_team_history():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_insert_query = """
        INSERT INTO team_history (
            team_id,
            fixture_id,
            match_date,
            team_name,
            away_team_id,
            away_team_name,
            goals_home,
            goals_away,
            yellow_cards_home,
            yellow_cards_away,
            red_cards_home,
            red_cards_away,
            corner_home,
            corner_away,
            team_strength_home,
            team_strength_away,
            match_result
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """
    
    formatted_data = [
        (
            item['team_id'], item['fixture_id'], item['match_date'], item['team_name'],
            item['away_team_id'], item['away_team_name'], item['goals_home'], item['goals_away'],
            item['yellow_cards_home'], item['yellow_cards_away'], item['red_cards_home'], item['red_cards_away'],
            item['corner_home'], item['corner_away'],
            item['team_strength_home'], item['team_strength_away'], item['match_result']
        )
        for item in data
    ]
    
    cursor.executemany(sql_insert_query, formatted_data)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Inserted success!"}), 201

@api_bp.route('/teams', methods=['POST'])
def insert_team(): 
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    sql_insert_query = """
        INSERT INTO team (
            team_id,
            team_name,
            logo
        ) VALUES (
            %s, %s, %s
        )
    """
    
    formatted_data = [
        (
            item['team_id'], item['team_name'], item['logo']
        )
        for item in data
    ]
    
    cursor.executemany(sql_insert_query, formatted_data)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Inserted success!"}), 201

@api_bp.route('/teams', methods=['GET'])
def read_teams():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM team"
    cursor.execute(sql)
    records = cursor.fetchall()
    return jsonify({'data': records}), 200

@api_bp.route('/trend/<int:team_id>', methods=['GET'])
def trend(team_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
    SELECT match_date, goals_home, yellow_cards_home, red_cards_home, corner_home
    FROM team_history
    WHERE team_id = %s
    ORDER BY match_date DESC
    """
    df = pd.read_sql(sql, conn, params=(team_id,))
    conn.close()
    df['match_date'] = pd.to_datetime(df['match_date'])
    return jsonify({'data': df.to_dict(orient='records')}), 200

@api_bp.route('/seasonal/<int:team_id>', methods=['GET'])
def get_seasonal_analysis(team_id):
    # Kết nối tới MySQL
    connection = get_db_connection()

    # Truy vấn dữ liệu từ bảng team_history
    query = """
    SELECT match_date, goals_home
    FROM team_history
    WHERE team_id = %s
    """
    df = pd.read_sql(query, connection, params=(team_id,))
    connection.close()

    # Chuyển cột match_date sang kiểu datetime
    df['match_date'] = pd.to_datetime(df['match_date'])
    df.set_index('match_date', inplace=True)

    # Đảm bảo dữ liệu có định dạng time series
    df = df.resample('M').mean() 

    # Xử lý giá trị thiếu (NaN)
    if df['goals_home'].isna().sum() > 0:
        df['goals_home'] = df['goals_home'].interpolate(method='linear')  # Nội suy giá trị thiếu

    # Phân tích Seasonal Decomposition  
    result = seasonal_decompose(df['goals_home'], model='additive', period=12)

    # Chuyển đổi seasonal component từ Series sang DataFrame
    seasonal_df = result.seasonal.reset_index()  # Reset index để biến `match_date` thành cột

    # Chuyển DataFrame sang dạng dictionary
    data = seasonal_df.to_dict(orient='records')

    # Trả về dữ liệu JSON
    return jsonify(data)

@api_bp.route('/weekly-stats/<int:team_id>', methods=['GET'])
def get_weekly_stats(team_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT match_date, goals_home, yellow_cards_home, red_cards_home, corner_home
        FROM team_history
        WHERE team_id = %s AND match_date >= '2024-01-01'
        ORDER BY match_date ASC;
    """
    df = pd.read_sql(query, conn, params=(team_id,))
    conn.close()

    df['match_date'] = pd.to_datetime(df['match_date'])

    # Nhóm dữ liệu theo tuần và tính tổng
    df['week'] = df['match_date'].dt.to_period('W')
    weekly_data = df.groupby('week')[['goals_home', 'yellow_cards_home', 'red_cards_home', 'corner_home']].sum()

    # Chuyển tuần thành chuỗi để chuẩn bị trả về
    weekly_data.reset_index(inplace=True)
    weekly_data['week'] = weekly_data['week'].astype(str)

    return jsonify(weekly_data.to_dict(orient='records'))

@api_bp.route('/daily-stats/<int:team_id>', methods=['GET'])
def get_daily_stats(team_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT match_date, goals_home, yellow_cards_home, red_cards_home, corner_home
        FROM team_history
        WHERE team_id = %s AND match_date >= '2024-01-01'
        ORDER BY match_date ASC;
    """
    df = pd.read_sql(query, conn, params=(team_id,))
    conn.close()

    df['match_date'] = pd.to_datetime(df['match_date'])

    daily_data = df.groupby('match_date')[['goals_home', 'yellow_cards_home', 'red_cards_home', 'corner_home']].sum()
    daily_data.reset_index(inplace=True)
    daily_data['match_date'] = daily_data['match_date'].astype(str)
    return jsonify(daily_data.to_dict(orient='records'))

@api_bp.route('/monthly-stats/<int:team_id>', methods=['GET'])
def get_monthly_stats(team_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT match_date, goals_home, yellow_cards_home, red_cards_home, corner_home
        FROM team_history
        WHERE team_id = %s AND match_date >= '2024-01-01'
        ORDER BY match_date ASC;
    """
    df = pd.read_sql(query, conn, params=(team_id,))
    conn.close()

    df['match_date'] = pd.to_datetime(df['match_date'])

    df['month'] = df['match_date'].dt.to_period('M')  
    monthly_data = df.groupby('month')[['goals_home', 'yellow_cards_home', 'red_cards_home', 'corner_home']].sum()
    monthly_data.reset_index(inplace=True)
    monthly_data['month'] = monthly_data['month'].astype(str)  

    return jsonify(monthly_data.to_dict(orient='records'))

@api_bp.route('/correlation', methods=['GET'])
def get_correlation():
    # Kết nối tới MySQL
    connection = get_db_connection()

    # Truy vấn dữ liệu từ bảng team_history
    query = """
    SELECT team_name, away_team_name, away_team_id, goals_home, yellow_cards_home, red_cards_home, corner_home,
           goals_away, yellow_cards_away, red_cards_away, corner_away, team_strength_home, team_strength_away, match_result
    FROM team_history
    """
    df = pd.read_sql(query, connection)
    connection.close()

    # Mã hóa cột match_result
    result_mapping = {'WIN': 1, 'DRAW': 0, 'LOSE': -1}
    df['match_result_encoded'] = df['match_result'].map(result_mapping)

    # Mã hóa cột away_team_name
    label_encoder = LabelEncoder()
    df['away_team_name_encoded'] = label_encoder.fit_transform(df['away_team_name'])

    # Chỉ lấy các cột số
    numerical_df = df.select_dtypes(include=['number'])

    # Tính ma trận tương quan
    correlation_matrix = numerical_df.corr()

    # Lấy tương quan của cột match_result_encoded với các cột khác
    correlation_with_match_result = correlation_matrix['match_result_encoded'].drop('match_result_encoded')

    # Chuyển đổi thành dictionary để trả về JSON
    correlation_dict = correlation_with_match_result.to_dict()

    return jsonify(correlation_dict)

@api_bp.route('/spider-chart/<int:home>/<int:away>', methods=['GET'])
def get_spider_chart_data(home, away):
    # Kết nối tới MySQL
    connection = get_db_connection()

    # Truy vấn dữ liệu chỉ lấy 1 bản ghi
    query = """
    SELECT 
           team_strength_home / 10 AS team_strength_home, 
           team_strength_away / 10 AS team_strength_away, 
           yellow_cards_home + red_cards_home AS total_cards_home, 
           yellow_cards_away + red_cards_away AS total_cards_away,
           corner_home AS total_corners_home, 
           corner_away AS total_corners_away,
           goals_home AS total_goals_home,
           goals_away AS total_goals_away
    FROM team_history
    WHERE team_id = %s AND away_team_id = %s
    LIMIT 5
    """
    df = pd.read_sql(query, connection, params=(home, away))
    connection.close()

    # Kiểm tra nếu không có bản ghi nào
    if df.empty:
        return jsonify({"error": "No record found."}), 404

    # Xử lý dữ liệu
    records = []
    for index, row in df.iterrows():
        record = {
            "Strength (1:10)": [row["team_strength_home"], row["team_strength_away"]],
            "Total Cards": [row["total_cards_home"], row["total_cards_away"]],
            "Total Corners": [row["total_corners_home"], row["total_corners_away"]],
            "Total Goals": [row["total_goals_home"], row["total_goals_away"]],
        }
        records.append(record)

    return jsonify(records)

def calculate_team_points(df):
    """Hàm tính điểm cho từng đội bóng."""
    team_points = {}
    
    for _, row in df.iterrows():
        team_id = row['team_id']
        match_result = row['match_result']
        
        if team_id not in team_points:
            team_points[team_id] = 0
        if match_result == 'WIN':
            team_points[team_id] += 3
        elif match_result == 'DRAW':
            team_points[team_id] += 1
    
    points_array = [{'team_id': team_id, 'points': points} for team_id, points in team_points.items()]
    return points_array

@api_bp.route('/rank/<int:team_id>', methods=['GET'])
def get_team_rank(team_id):
    
    connection = get_db_connection()
    query = """
    SELECT team_id, match_result
    FROM team_history
    WHERE match_date >= '2024-08-01'
    """
    df = pd.read_sql(query, connection)
    connection.close()
    
    # Tính toán điểm
    points_array = calculate_team_points(df)
    sorted_teams = sorted(points_array, key=lambda x: x['points'], reverse=True)

    team_ids = [team['team_id'] for team in sorted_teams]
    points = [team['points'] for team in sorted_teams]

    return jsonify({'team_ids': team_ids, 'points': points}), 200
    
    # Tìm thứ hạng của team_id
    # for index, team in enumerate(sorted_teams, start=1):
    #     return jsonify({"team_id": team_id, "rank": index, "points": team['points']})

@api_bp.route('/predict/<int:home>/<int:away>', methods=['GET'])
def predict_next_match(home, away):
    # Kết nối tới MySQL
    connection = get_db_connection()

    query = """
    SELECT 
            team_id,
            away_team_id,
           team_strength_home, 
           team_strength_away, 
           yellow_cards_home + red_cards_home AS cards_home, 
           yellow_cards_away + red_cards_away AS cards_away,
           corner_home AS corners_home, 
           corner_away AS corners_away,
           goals_home AS goals_home,
           goals_away AS goals_away,
           match_result
    FROM team_history
    WHERE team_id = %s
    ORDER BY match_date DESC
    LIMIT 10;
    """

    df_home = pd.read_sql(query, connection, params=(home,))
    df_away = pd.read_sql(query, connection, params=(away,))

    df = pd.concat([df_home, df_away])

    connection.close()

    # Tách dữ liệu thành đầu vào (X) và đầu ra (y)
    X = df[["team_strength_home", "team_strength_away"]]

    y_goals_home = df["goals_home"]
    y_goals_away = df["goals_away"]
    y_corners_home = df["corners_home"]
    y_corners_away = df["corners_away"]
    y_cards_home = df["cards_home"]
    y_cards_away = df["cards_away"]

    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, _, y_goals_home_train, _ = train_test_split(X, y_goals_home, test_size=0.2, random_state=42)
    _, _, y_goals_away_train, _ = train_test_split(X, y_goals_away, test_size=0.2, random_state=42)
    _, _, y_corners_home_train, _ = train_test_split(X, y_corners_home, test_size=0.2, random_state=42)
    _, _, y_corners_away_train, _ = train_test_split(X, y_corners_away, test_size=0.2, random_state=42)
    _, _, y_cards_home_train, _ = train_test_split(X, y_cards_home, test_size=0.2, random_state=42)
    _, _, y_cards_away_train, _ = train_test_split(X, y_cards_away, test_size=0.2, random_state=42)

    # Huấn luyện mô hình RandomForest cho từng giá trị
    model_goals_home = RandomForestRegressor(random_state=42)
    model_goals_away = RandomForestRegressor(random_state=42)
    model_corners_home = RandomForestRegressor(random_state=42)
    model_corners_away = RandomForestRegressor(random_state=42)
    model_cards_home = RandomForestRegressor(random_state=42)
    model_cards_away = RandomForestRegressor(random_state=42)

    model_goals_home.fit(X_train, y_goals_home_train)
    model_goals_away.fit(X_train, y_goals_away_train)
    model_corners_home.fit(X_train, y_corners_home_train)
    model_corners_away.fit(X_train, y_corners_away_train)
    model_cards_home.fit(X_train, y_cards_home_train)
    model_cards_away.fit(X_train, y_cards_away_train)

    # Truy vấn sức mạnh của các đội từ dữ liệu
    home_team_strength = df.iloc[0]["team_strength_home"]
    away_team_strength = df.iloc[0]["team_strength_away"]

    # Dự đoán dựa trên sức mạnh của hai đội
    # next_match = pd.DataFrame({
    #     "team_strength_home": [home_team_strength],
    #     "team_strength_away": [away_team_strength]
    # })

    next_match = pd.DataFrame({
        "team_strength_home": [100],
        "team_strength_away": [100]
    })

    predictions = {
        "predicted_goals_home": round(model_goals_home.predict(next_match)[0]),
        "predicted_goals_away": round(model_goals_away.predict(next_match)[0]),
        "predicted_corners_home": round(model_corners_home.predict(next_match)[0]),
        "predicted_corners_away": round(model_corners_away.predict(next_match)[0]),
        "predicted_cards_home": round(model_cards_home.predict(next_match)[0]),
        "predicted_cards_away": round(model_cards_away.predict(next_match)[0]),
    }

    return jsonify(predictions)

@api_bp.route('/check-fixture-id/<int:fixture_id>', methods=['GET'])
def check_fixture_id(fixture_id):
    try:
        # Kết nối cơ sở dữ liệu
        connection = get_db_connection()
        cursor = connection.cursor()

        # Câu lệnh truy vấn
        query = """
        SELECT 
            fixture_id
        FROM 
            team_history
        WHERE 
            fixture_id = %s
        """
        cursor.execute(query, (fixture_id,))
        result = cursor.fetchall()  # Lấy một dòng kết quả

        # Đóng cursor và connection
        cursor.close()
        connection.close()

        # Xử lý kết quả
        if result:
            return jsonify({"exists": True, "message": "Fixture ID exists in the database"}), 200
        else:
            return jsonify({"exists": False, "message": "Fixture ID does not exist in the database"}), 404

    except Exception as e:
        # Xử lý lỗi
        return jsonify({"error": str(e)}), 500

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='localhost')