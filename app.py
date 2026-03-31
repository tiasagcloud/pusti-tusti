from flask import Flask, jsonify, request
import pandas as pd
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Load food data
df = pd.read_excel("foods.xlsx")

# DATABASE for daily logs
conn = sqlite3.connect('nutrition.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS daily_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id INTEGER,
    food_name TEXT,
    calories REAL,
    protein REAL,
    carbs REAL,
    fats REAL,
    date TEXT
)
''')

# API: Get food details
@app.route('/food/<int:food_id>')
def get_food(food_id):
    food = df[df['food_id'] == food_id].to_dict(orient='records')
    
    if food:
        return jsonify(food[0])
    return jsonify({"error": "Food not found"})

# API: Save scanned food
@app.route('/log', methods=['POST'])
def log_food():
    data = request.json
    
    cursor.execute('''
    INSERT INTO daily_log (food_id, food_name, calories, protein, carbs, fats, date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['food_id'],
        data['food_name'],
        data['calories'],
        data['protein'],
        data['carbs'],
        data['fats'],
        datetime.now().strftime("%Y-%m-%d")
    ))
    
    conn.commit()
    
    return {"message": "Saved successfully"}

# API: Daily summary
@app.route('/daily-summary')
def summary():
    today = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute('''
    SELECT SUM(calories), SUM(protein), SUM(carbs), SUM(fats)
    FROM daily_log WHERE date=?
    ''', (today,))
    
    result = cursor.fetchone()
    
    return jsonify({
        "calories": result[0] or 0,
        "protein": result[1] or 0,
        "carbs": result[2] or 0,
        "fats": result[3] or 0
    })

if __name__ == '__main__':
    app.run(debug=True)