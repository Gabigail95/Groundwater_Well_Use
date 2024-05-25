from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

# Retrieve data from stations.db
def get_well_use_counts():
    conn = sqlite3.connect('stations.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT well_use, COUNT(DISTINCT site_code) as count
        FROM stations
        WHERE well_use != 'Unknown'
        GROUP BY well_use
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

# Retrieve distinct years from merged_data.db
def get_years():
    conn = sqlite3.connect('merged_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT strftime('%Y', msmt_date) as year
        FROM merged_data
        ORDER BY year
    ''')
    years = [row[0] for row in cursor.fetchall()]
    conn.close()
    return years

# Retrieve data for the second chart from merged_data.db
def get_second_chart_data(year1, year2):
    conn = sqlite3.connect('merged_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT well_use, 
               AVG(CASE WHEN strftime('%Y', msmt_date) = ? THEN gwe END) as avg_gwe_year1,
               AVG(CASE WHEN strftime('%Y', msmt_date) = ? THEN gwe END) as avg_gwe_year2
        FROM merged_data
        WHERE well_use != 'Unknown'
        GROUP BY well_use
    ''', (year1, year2))
    result = cursor.fetchall()
    conn.close()
    return result

@app.route('/data')
def data():
    well_use_counts = get_well_use_counts()
    data = {'labels': [], 'counts': []}
    for row in well_use_counts:
        data['labels'].append(row[0])
        data['counts'].append(row[1])
    return jsonify(data)

@app.route('/second_chart_data')
def second_chart_data():
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')
    if not year1 or not year2:
        return jsonify({'error': 'Both year1 and year2 are required'}), 400
    second_chart_data = get_second_chart_data(year1, year2)
    data = {'labels': [], 'avg_gwe_year1': [], 'avg_gwe_year2': []}
    for row in second_chart_data:
        data['labels'].append(row[0])
        data['avg_gwe_year1'].append(row[1] if row[1] is not None else 0)
        data['avg_gwe_year2'].append(row[2] if row[2] is not None else 0)
    return jsonify(data)

@app.route('/')
def index():
    years = get_years()
    return render_template('index.html', years=years)

if __name__ == '__main__':
    app.run(debug=True)
