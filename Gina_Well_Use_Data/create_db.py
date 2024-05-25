import sqlite3
import csv

# Read the CSV file and insert data into the database
def create_db(csv_file, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stations (
            site_code TEXT,
            stn_id INTEGER,
            swn TEXT,
            well_name TEXT,
            continuous_data_station_number INTEGER,
            latitude REAL,
            longitude REAL,
            gse REAL,
            rpe REAL,
            gse_method TEXT,
            gse_acc TEXT,
            basin_code TEXT,
            basin_name TEXT,
            county_name TEXT,
            well_depth REAL,
            well_use TEXT,
            well_type TEXT,
            wcr_no TEXT,
            monitoring_program TEXT
        )
    ''')

    # Read data from CSV and insert into table
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            values = [row[field] for field in reader.fieldnames]
            cursor.execute('INSERT INTO stations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)

    conn.commit()
    conn.close()

    print("Database created and data inserted successfully.")

if __name__ == "__main__":
    create_db('stations.csv', 'stations.db')
