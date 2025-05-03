import pandas as pd
import sqlite3

# Load Excel file
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')  # update sheet_name if needed

# Connect to SQLite database (or create it)
conn = sqlite3.connect('output.db')
cursor = conn.cursor()

# Create table based on dataframe columns
table_name = 'your_table'
columns = ', '.join([f'"{col}" TEXT' for col in df.columns])
cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns});')

# Insert data into table
for _, row in df.iterrows():
    placeholders = ', '.join(['?'] * len(row))
    sql = f'INSERT INTO {table_name} VALUES ({placeholders})'
    cursor.execute(sql, tuple(row))

# Commit and close
conn.commit()
conn.close()

