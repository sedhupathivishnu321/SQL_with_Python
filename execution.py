import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("output.db")  # Change to your file name

# Load entire table
df = pd.read_sql_query("SELECT * FROM your_table", conn)

# Define grading function
def get_grade(mark):
    try:
        m = int(mark)
        if m > 95:
            return 'O+'
        elif m > 85:
            return 'O'
        elif m > 75:
            return 'A'
        else:
            return 'B'
    except:
        return 'Invalid'

# Apply grade calculation to each subject
for subject in ['Tamil', 'English', 'Maths', 'Science', 'Social']:
    grade_col = subject + '_Grade'
    df[grade_col] = df[subject].apply(get_grade)

# Show in console
print("📊 Student Marks with Grades:")
print(df)

# Export to Excel
output_file = "student_marks_with_grades.xlsx"
df.to_excel(output_file, index=False)
print(f"✅ Report saved as: {output_file}")

# Close connection
conn.close()
