"""
Setup script to create multiple teachers and distribute students across different exam halls.
Creates teachers: teacher_adm303, teacher1, teacher2, teacher3
Halls: ADM 303, ADM 304, ADM 305, ADM 306
Each hall has students from different departments with proper roll number formats.
"""

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.Studetails
students = db.student
teachers = db.teacher

sample_date = '18.11.2025'

# Define teachers and their halls
teachers_config = [
    {'username': 'teacher_adm303', 'password': 'demo123', 'name': 'Demo Teacher ADM303', 'hall': 'ADM 303'},
    {'username': 'teacher1', 'password': 'demo123', 'name': 'Teacher 1 ADM304', 'hall': 'ADM 304'},
    {'username': 'teacher2', 'password': 'demo123', 'name': 'Teacher 2 ADM305', 'hall': 'ADM 305'},
    {'username': 'teacher3', 'password': 'demo123', 'name': 'Teacher 3 ADM306', 'hall': 'ADM 306'},
]

# Insert or update teachers
print("Setting up teachers...")
for t_config in teachers_config:
    teachers.update_one(
        {'username': t_config['username']},
        {'$set': {
            'username': t_config['username'],
            'password': t_config['password'],
            'name': t_config['name'],
            'invigilation_hall': t_config['hall']
        }},
        upsert=True
    )
    print(f"  ✓ {t_config['username']} → {t_config['hall']}")

# Define student batches for each hall with department information
halls_config = [
    {
        'hall': 'ADM 303',
        'batches': [
            {'dept_name': 'AIDS', 'dept_code': '2218', 'count': 20, 'subjects': ['EC19702', 'CS19501']},
            {'dept_name': 'AIML', 'dept_code': '2215', 'count': 20, 'subjects': ['IT19741', 'ME19601']},
        ]
    },
    {
        'hall': 'ADM 304',
        'batches': [
            {'dept_name': 'CSE', 'dept_code': '2213', 'count': 20, 'subjects': ['CS19501', 'CE19401']},
            {'dept_name': 'ECE', 'dept_code': '2218', 'count': 20, 'subjects': ['EC19702', 'EE19301']},
        ]
    },
    {
        'hall': 'ADM 305',
        'batches': [
            {'dept_name': 'MECH', 'dept_code': '2219', 'count': 20, 'subjects': ['ME19601', 'EC19702']},
            {'dept_name': 'CIVIL', 'dept_code': '2220', 'count': 20, 'subjects': ['CE19401', 'IT19741']},
        ]
    },
    {
        'hall': 'ADM 306',
        'batches': [
            {'dept_name': 'EEE', 'dept_code': '2221', 'count': 20, 'subjects': ['EE19301', 'CS19501']},
            {'dept_name': 'BIO', 'dept_code': '2222', 'count': 20, 'subjects': ['EC19702', 'IT19741']},
        ]
    },
]

# Insert students for each hall
print("\nSetting up students and seating...")
cols = ['A', 'B', 'C', 'D', 'E']
benches = [1, 2, 3, 4]

for hall_config in halls_config:
    hall = hall_config['hall']

    # Remove previous students for this hall
    students.delete_many({'seatnum.classroom': hall})

    print(f"\n  Hall: {hall}")

    # Expect two departments per hall; seat 20 students from each department here.
    if len(hall_config['batches']) < 2:
        continue
    left_batch = hall_config['batches'][0]
    right_batch = hall_config['batches'][1]

    left_base = int(f"{left_batch['dept_code']}010")
    right_base = int(f"{right_batch['dept_code']}010")

    left_seq = 1
    right_seq = 1
    left_needed = 20
    right_needed = 20

    # Fill benches, columns; Left seat gets left_dept, Right seat gets right_dept — this interleaves departments per bench.
    for b in benches:
        for col in cols:
            # Left seat
            if left_needed > 0:
                roll_left = left_base * 100 + left_seq
                subj = left_batch['subjects'][(left_seq - 1) % len(left_batch['subjects'])]
                seat_label = f"{col}L{b}"
                doc_left = {
                    'rollnum': int(roll_left),
                    'name': f"STU_{left_batch['dept_name']}_{roll_left}",
                    'Year': 'FourthYear',
                    'branch': left_batch['dept_name'],
                    'department': left_batch['dept_code'],
                    'seatnum': [
                        {
                            'date': sample_date,
                            'seatnum': seat_label,
                            'seat_label': seat_label[:2],
                            'bench_number': b,
                            'column_letter': col,
                            'side': 'Left',
                            'classroom': hall,
                            'subject': subj
                        }
                    ]
                }
                students.replace_one({'rollnum': int(roll_left)}, doc_left, upsert=True)
                left_seq += 1
                left_needed -= 1

            # Right seat
            if right_needed > 0:
                roll_right = right_base * 100 + right_seq
                subj = right_batch['subjects'][(right_seq - 1) % len(right_batch['subjects'])]
                seat_label = f"{col}R{b}"
                doc_right = {
                    'rollnum': int(roll_right),
                    'name': f"STU_{right_batch['dept_name']}_{roll_right}",
                    'Year': 'FourthYear',
                    'branch': right_batch['dept_name'],
                    'department': right_batch['dept_code'],
                    'seatnum': [
                        {
                            'date': sample_date,
                            'seatnum': seat_label,
                            'seat_label': seat_label[:2],
                            'bench_number': b,
                            'column_letter': col,
                            'side': 'Right',
                            'classroom': hall,
                            'subject': subj
                        }
                    ]
                }
                students.replace_one({'rollnum': int(roll_right)}, doc_right, upsert=True)
                right_seq += 1
                right_needed -= 1

            if left_needed <= 0 and right_needed <= 0:
                break
        if left_needed <= 0 and right_needed <= 0:
            break

    print(f"    ✓ {left_batch['dept_name']} (Code: {left_batch['dept_code']}): 20 students assigned")
    print(f"    ✓ {right_batch['dept_name']} (Code: {right_batch['dept_code']}): 20 students assigned")

print("\n✅ Setup Complete!")
print("\nTeacher Credentials:")
for t_config in teachers_config:
    print(f"  Username: {t_config['username']}, Password: {t_config['password']}, Hall: {t_config['hall']}")

print("\nDepartments by Hall:")
print("  ADM 303: AIDS (2218), AIML (2215)")
print("  ADM 304: CSE (2213), ECE (2218)")
print("  ADM 305: MECH (2219), CIVIL (2220)")
print("  ADM 306: EEE (2221), BIO (2222)")

print("\nRoll Number Format Examples:")
print("  AIDS (2218): 221801001, 221801002, ..., 221801020")
print("  AIML (2215): 221501001, 221501002, ..., 221501020")
print("  CSE (2213): 221301001, 221301002, ..., 221301020")

print("\nNext steps:")
print("1. Start the Flask app: python app.py")
print("2. Visit http://127.0.0.1:5000/teacher/login")
print("3. Login with any of the teacher accounts above")
print("4. Select date 18.11.2025 to view seating")

