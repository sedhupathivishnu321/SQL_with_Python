import sqlite3
import pandas as pd

# Step 1: Load CSV file
csv_path = r"C:\Users\sedhu\Desktop\AMIT\students.csv"  # Replace with your actual file path
df = pd.read_csv(csv_path)

# Step 2: Connect to SQLite database (or create it)
conn = sqlite3.connect("output_1.db")  # You can rename this file
cursor = conn.cursor()

# Step 3: Create table and insert data
table_name = "students"  # You can change this
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Step 4: Verify the data (optional)
print(f"✅ Table '{table_name}' created with {len(df)} rows.")
result = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)
print(result)

# Step 5: Close connection
conn.close()
