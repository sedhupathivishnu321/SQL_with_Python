import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Create the students table
def create_students_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            standard TEXT
        )
    """)
    conn.commit()

# Step 2: Insert sample data
def insert_sample_students(conn):
    sample_data = [
        (1, 'Alice', 14, 'F', '8'),
        (2, 'Bob', 15, 'M', '9'),
        (3, 'Charlie', 14, 'M', '8'),
        (4, 'Daisy', 13, 'F', '7'),
        (5, 'Ethan', 14, 'M', '8')
    ]
    conn.executemany("INSERT OR IGNORE INTO students VALUES (?, ?, ?, ?, ?)", sample_data)
    conn.commit()

# Step 3: Retrieve data and visualize
def visualize_and_save_students(conn):
    # Load data into DataFrame
    df = pd.read_sql_query("SELECT * FROM students", conn)

    # Save data to CSV
    df.to_csv("students.csv", index=False)
    print("✅ Data saved to students.csv")

    # Create a bar chart of students per standard
    count_df = df['standard'].value_counts().sort_index()
    plt.figure(figsize=(8, 5))
    count_df.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Number of Students per Standard")
    plt.xlabel("Standard")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig("students_Chart.png")
    plt.show()
    print("📊 Chart saved to students_per_standard.png")

# Main execution
if __name__ == "__main__":
    conn = sqlite3.connect("demo.db")
    create_students_table(conn)
    insert_sample_students(conn)
    visualize_and_save_students(conn)
    conn.close()
