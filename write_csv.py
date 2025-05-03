import csv

data = [
    ['Roll No', 'Name', 'age', 'Marks'],
    [1, 'Alice',20, 85],
    [2, 'Bob',20, 90],
]
with open('students.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
with open('output.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
