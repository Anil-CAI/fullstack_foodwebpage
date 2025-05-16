import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('D:/Workspace/maha_rest/database/maha_rest.db')

# Get a list of all table names in the database
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Display each table's data using pandas
for table_name in tables:
    table_name = table_name[0]  # Extract table name from tuple
    print(f"\n===== TABLE: {table_name.upper()} =====")
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        print(df)
    except Exception as e:
        print(f"Failed to read table {table_name}: {e}")

# Close the connection
conn.close()
