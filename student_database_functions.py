import sqlite3
import pandas as pd

def connect_db(db_name="output.db"):
    return sqlite3.connect(db_name)

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

def create_subjects_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT
        )
    """)
    conn.commit()

def create_marks_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            roll_no INTEGER,
            subject_id INTEGER,
            marks INTEGER,
            FOREIGN KEY(roll_no) REFERENCES students(roll_no),
            FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
        )
    """)
    conn.commit()

def add_new_student_record(conn, roll_no, name, age, gender, standard):
    conn.execute("INSERT INTO students (roll_no, name, age, gender, standard) VALUES (?, ?, ?, ?, ?)",
                 (roll_no, name, age, gender, standard))
    conn.commit()

def update_student_grade(conn, roll_no, subject_id, new_marks):
    conn.execute("UPDATE marks SET marks = ? WHERE roll_no = ? AND subject_id = ?",
                 (new_marks, roll_no, subject_id))
    conn.commit()

def delete_student_by_roll_number(conn, roll_no):
    conn.execute("DELETE FROM marks WHERE roll_no = ?", (roll_no,))
    conn.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
    conn.commit()

def search_student_by_name(conn, name):
    return conn.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + name + '%',)).fetchall()

def list_all_students_in_standard(conn, standard):
    return conn.execute("SELECT * FROM students WHERE standard = ?", (standard,)).fetchall()

def calculate_average_marks(conn, roll_no):
    return conn.execute("SELECT AVG(marks) FROM marks WHERE roll_no = ?", (roll_no,)).fetchone()[0]

def find_top_scorer_each_subject(conn):
    return conn.execute("""
        SELECT s.subject_name, st.name, MAX(m.marks)
        FROM marks m
        JOIN students st ON m.roll_no = st.roll_no
        JOIN subjects s ON m.subject_id = s.subject_id
        GROUP BY m.subject_id
    """).fetchall()

def generate_report_card(conn, roll_no):
    return conn.execute("""
        SELECT s.subject_name, m.marks
        FROM marks m
        JOIN subjects s ON m.subject_id = s.subject_id
        WHERE m.roll_no = ?
    """, (roll_no,)).fetchall()

def list_students_with_failing_marks(conn, threshold=35):
    return conn.execute("""
        SELECT DISTINCT st.roll_no, st.name, m.marks
        FROM marks m
        JOIN students st ON m.roll_no = st.roll_no
        WHERE m.marks < ?
    """, (threshold,)).fetchall()

def rank_students_by_total_marks(conn):
    return conn.execute("""
        SELECT st.roll_no, st.name, SUM(m.marks) as total
        FROM marks m
        JOIN students st ON m.roll_no = st.roll_no
        GROUP BY st.roll_no
        ORDER BY total DESC
    """).fetchall()

def insert_multiple_students(conn, student_list):
    conn.executemany("INSERT INTO students (roll_no, name, age, gender, standard) VALUES (?, ?, ?, ?, ?)", student_list)
    conn.commit()

def join_student_and_marks_table(conn):
    return conn.execute("""
        SELECT st.roll_no, st.name, s.subject_name, m.marks
        FROM marks m
        JOIN students st ON m.roll_no = st.roll_no
        JOIN subjects s ON m.subject_id = s.subject_id
    """).fetchall()

def gender_wise_performance_stats(conn):
    return conn.execute("""
        SELECT st.gender, AVG(m.marks)
        FROM students st
        JOIN marks m ON st.roll_no = m.roll_no
        GROUP BY st.gender
    """).fetchall()

def age_distribution_analysis(conn):
    return conn.execute("SELECT age, COUNT(*) FROM students GROUP BY age").fetchall()

def subject_wise_topper_list(conn):
    return conn.execute("""
        SELECT s.subject_name, st.name, m.marks
        FROM marks m
        JOIN students st ON m.roll_no = st.roll_no
        JOIN subjects s ON m.subject_id = s.subject_id
        WHERE (m.subject_id, m.marks) IN (
            SELECT subject_id, MAX(marks) FROM marks GROUP BY subject_id
        )
    """).fetchall()

def students_scoring_above_90(conn):
    return conn.execute("""
        SELECT DISTINCT st.roll_no, st.name
        FROM marks m
        JOIN students st ON m.roll_no = st.roll_no
        WHERE m.marks > 90
    """).fetchall()

def add_remarks_column(conn):
    conn.execute("ALTER TABLE students ADD COLUMN remarks TEXT")
    conn.commit()

def create_attendance_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            roll_no INTEGER,
            date TEXT,
            present INTEGER,
            FOREIGN KEY(roll_no) REFERENCES students(roll_no)
        )
    """)
    conn.commit()

def find_students_with_full_attendance(conn):
    return conn.execute("""
        SELECT roll_no FROM attendance
        GROUP BY roll_no
        HAVING SUM(present) = COUNT(*)
    """).fetchall()

def list_students_by_age_group(conn):
    return conn.execute("""
        SELECT CASE
            WHEN age < 10 THEN 'Under 10'
            WHEN age BETWEEN 10 AND 15 THEN '10-15'
            ELSE '15+'
        END as age_group, COUNT(*)
        FROM students
        GROUP BY age_group
    """).fetchall()

def standard_wise_average_marks(conn):
    return conn.execute("""
        SELECT standard, AVG(marks)
        FROM students s
        JOIN marks m ON s.roll_no = m.roll_no
        GROUP BY standard
    """).fetchall()

def insert_parent_contact_info(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS parents (
            roll_no INTEGER,
            parent_name TEXT,
            contact TEXT,
            FOREIGN KEY(roll_no) REFERENCES students(roll_no)
        )
    """)
    conn.commit()

def query_parent_details(conn):
    return conn.execute("""
        SELECT s.name, p.parent_name, p.contact
        FROM students s
        JOIN parents p ON s.roll_no = p.roll_no
    """).fetchall()

def delete_students_below_pass_mark(conn, threshold=35):
    conn.execute("""
        DELETE FROM students
        WHERE roll_no IN (
            SELECT roll_no FROM marks GROUP BY roll_no HAVING MIN(marks) < ?
        )
    """, (threshold,))
    conn.commit()

def group_students_by_grade(conn):
    return conn.execute("""
        SELECT name,
        CASE
            WHEN AVG(marks) >= 90 THEN 'A'
            WHEN AVG(marks) >= 75 THEN 'B'
            WHEN AVG(marks) >= 60 THEN 'C'
            ELSE 'D'
        END AS grade
        FROM students s
        JOIN marks m ON s.roll_no = m.roll_no
        GROUP BY s.roll_no
    """).fetchall()

def create_backup_of_student_data(conn, filename="backup.csv"):
    df = pd.read_sql_query("SELECT * FROM students", conn)
    df.to_csv(filename, index=False)

def update_subject_names(conn, old_name, new_name):
    conn.execute("UPDATE subjects SET subject_name = ? WHERE subject_name = ?", (new_name, old_name))
    conn.commit()

def create_teachers_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            subject_id INTEGER,
            FOREIGN KEY(subject_id) REFERENCES subjects(subject_id)
        )
    """)
    conn.commit()

def assign_teacher_to_subject(conn, name, subject_id):
    conn.execute("INSERT INTO teachers (name, subject_id) VALUES (?, ?)", (name, subject_id))
    conn.commit()

def display_teacher_subject_mapping(conn):
    return conn.execute("""
        SELECT t.name, s.subject_name
        FROM teachers t
        JOIN subjects s ON t.subject_id = s.subject_id
    """).fetchall()

def subject_wise_class_average(conn):
    return conn.execute("""
        SELECT s.subject_name, st.standard, AVG(m.marks)
        FROM marks m
        JOIN students st ON m.roll_no = st.roll_no
        JOIN subjects s ON m.subject_id = s.subject_id
        GROUP BY s.subject_name, st.standard
    """).fetchall()

def top_3_students_per_class(conn):
    return conn.execute("""
        SELECT * FROM (
            SELECT st.roll_no, st.name, st.standard, SUM(m.marks) AS total,
                   RANK() OVER (PARTITION BY st.standard ORDER BY SUM(m.marks) DESC) as rank
            FROM students st
            JOIN marks m ON st.roll_no = m.roll_no
            GROUP BY st.roll_no
        ) WHERE rank <= 3
    """).fetchall()

def insert_new_subject(conn, subject_name):
    conn.execute("INSERT INTO subjects (subject_name) VALUES (?)", (subject_name,))
    conn.commit()

def change_roll_number_format(conn, prefix="S"):
    students = conn.execute("SELECT roll_no FROM students").fetchall()
    for (roll_no,) in students:
        new_roll_no = prefix + str(roll_no)
        conn.execute("UPDATE students SET roll_no = ? WHERE roll_no = ?", (new_roll_no, roll_no))
    conn.commit()

def search_by_partial_name(conn, partial_name):
    return conn.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + partial_name + '%',)).fetchall()

def store_health_check_data(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS health (
            roll_no INTEGER,
            bmi REAL,
            eye_vision TEXT,
            FOREIGN KEY(roll_no) REFERENCES students(roll_no)
        )
    """)
    conn.commit()

def find_students_with_perfect_score(conn):
    return conn.execute("""
        SELECT DISTINCT st.roll_no, st.name
        FROM marks m
        JOIN students st ON m.roll_no = st.roll_no
        GROUP BY st.roll_no
        HAVING MIN(marks) = 100 AND MAX(marks) = 100
    """).fetchall()

def list_failed_subjects_per_student(conn):
    return conn.execute("""
        SELECT st.roll_no, st.name, s.subject_name, m.marks
        FROM marks m
        JOIN students st ON m.roll_no = st.roll_no
        JOIN subjects s ON m.subject_id = s.subject_id
        WHERE m.marks < 35
    """).fetchall()

def track_disciplinary_records(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS discipline (
            roll_no INTEGER,
            incident TEXT,
            date TEXT,
            FOREIGN KEY(roll_no) REFERENCES students(roll_no)
        )
    """)
    conn.commit()

def generate_full_student_profile(conn, roll_no):
    student = conn.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,)).fetchone()
    marks = generate_report_card(conn, roll_no)
    return student, marks

def merge_academic_and_attendance_data(conn):
    return conn.execute("""
        SELECT st.roll_no, st.name, AVG(m.marks) as avg_marks, SUM(a.present) as total_present
        FROM students st
        LEFT JOIN marks m ON st.roll_no = m.roll_no
        LEFT JOIN attendance a ON st.roll_no = a.roll_no
        GROUP BY st.roll_no
    """).fetchall()

def filter_by_standard_and_gender(conn, standard, gender):
    return conn.execute("SELECT * FROM students WHERE standard = ? AND gender = ?", (standard, gender)).fetchall()

def calculate_grade_wise_pass_percentage(conn):
    return conn.execute("""
        SELECT standard,
            100.0 * SUM(CASE WHEN m.marks >= 35 THEN 1 ELSE 0 END) / COUNT(*) AS pass_percentage
        FROM students s
        JOIN marks m ON s.roll_no = m.roll_no
        GROUP BY s.standard
    """).fetchall()

def list_students_by_birthday_month(conn, month):
    return conn.execute("SELECT * FROM students WHERE strftime('%m', birthday) = ?", (month,)).fetchall()

def assign_section_to_student(conn):
    conn.execute("ALTER TABLE students ADD COLUMN section TEXT")
    conn.commit()

def find_duplicate_student_entries(conn):
    return conn.execute("""
        SELECT name, COUNT(*) FROM students
        GROUP BY name
        HAVING COUNT(*) > 1
    """).fetchall()

def log_modification_history(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS modification_log (
            roll_no INTEGER,
            change TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()

def calculate_overall_school_performance(conn):
    return conn.execute("SELECT AVG(marks) FROM marks").fetchone()[0]
