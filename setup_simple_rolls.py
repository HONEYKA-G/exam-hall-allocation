"""
Setup with simple sequential roll numbers (990001, 990002, etc.)
8 halls total: ADM 303, ADM 304, ADM 305, ADM 306, B212, B213, B218, B219
Two departments per hall, interleaved (Left dept + Right dept per bench)
"""

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.Studetails
students = db.student
teachers = db.teacher

sample_date = '18.11.2025'

# Define all 8 halls with their department pairs
halls_config = [
    {
        'hall': 'ADM 303',
        'teacher': 'teacher_adm303',
        'dept_left': ('ECE', 'EC19702'),
        'dept_right': ('IT', 'IT19741')
    },
    {
        'hall': 'ADM 304',
        'teacher': 'teacher1',
        'dept_left': ('CSE', 'CS19501'),
        'dept_right': ('MECH', 'ME19601')
    },
    {
        'hall': 'ADM 305',
        'teacher': 'teacher2',
        'dept_left': ('ECE', 'EC19702'),
        'dept_right': ('CIVIL', 'CE19401')
    },
    {
        'hall': 'ADM 306',
        'teacher': 'teacher3',
        'dept_left': ('IT', 'IT19741'),
        'dept_right': ('EEE', 'EE19301')
    },
    {
        'hall': 'B212',
        'teacher': 'teacher_b212',
        'dept_left': ('ECE', 'EC19702'),
        'dept_right': ('IT', 'IT19741')
    },
    {
        'hall': 'B213',
        'teacher': 'teacher_b213',
        'dept_left': ('CSE', 'CS19501'),
        'dept_right': ('MECH', 'ME19601')
    },
    {
        'hall': 'B218',
        'teacher': 'teacher_b218',
        'dept_left': ('ECE', 'EC19702'),
        'dept_right': ('CIVIL', 'CE19401')
    },
    {
        'hall': 'B219',
        'teacher': 'teacher_b219',
        'dept_left': ('IT', 'IT19741'),
        'dept_right': ('EEE', 'EE19301')
    },
]

# Clear all student/teacher collections and rebuild
students.delete_many({})
teachers.delete_many({})

print("Setting up 8 halls with simple sequential roll numbers...\n")

cols = ['A', 'B', 'C', 'D', 'E']
benches = [1, 2, 3, 4]
roll_counter = 990001

# For each hall, create teacher and assign 40 students (20 per department, interleaved L/R)
for hall_config in halls_config:
    hall = hall_config['hall']
    teacher_name = hall_config['teacher']
    left_dept_name, left_subject = hall_config['dept_left']
    right_dept_name, right_subject = hall_config['dept_right']
    
    # Create teacher
    teachers.insert_one({
        'username': teacher_name,
        'password': 'demo123',
        'name': f'Teacher {hall}',
        'invigilation_hall': hall
    })
    
    print(f"Hall: {hall}")
    print(f"  Departments: {left_dept_name} (Left) + {right_dept_name} (Right)")
    
    # Fill seats: 20 students from left_dept on left seats, 20 from right_dept on right seats
    left_count = 0
    right_count = 0
    
    for b in benches:
        for col in cols:
            # Left seat - left department
            if left_count < 20:
                roll = roll_counter
                roll_counter += 1
                seat_label = f"{col}L{b}"
                doc_left = {
                    'rollnum': int(roll),
                    'name': f'STU_{left_dept_name}_{roll}',
                    'Year': 'FourthYear',
                    'branch': left_dept_name,
                    'seatnum': [
                        {
                            'date': sample_date,
                            'seatnum': seat_label,
                            'seat_label': seat_label[:2],
                            'bench_number': b,
                            'column_letter': col,
                            'side': 'Left',
                            'classroom': hall,
                            'subject': left_subject
                        }
                    ]
                }
                students.insert_one(doc_left)
                left_count += 1
            
            # Right seat - right department
            if right_count < 20:
                roll = roll_counter
                roll_counter += 1
                seat_label = f"{col}R{b}"
                doc_right = {
                    'rollnum': int(roll),
                    'name': f'STU_{right_dept_name}_{roll}',
                    'Year': 'FourthYear',
                    'branch': right_dept_name,
                    'seatnum': [
                        {
                            'date': sample_date,
                            'seatnum': seat_label,
                            'seat_label': seat_label[:2],
                            'bench_number': b,
                            'column_letter': col,
                            'side': 'Right',
                            'classroom': hall,
                            'subject': right_subject
                        }
                    ]
                }
                students.insert_one(doc_right)
                right_count += 1
            
            if left_count >= 20 and right_count >= 20:
                break
        if left_count >= 20 and right_count >= 20:
            break
    
    print(f"  ✓ 40 students assigned (Rolls {roll_counter - 40}-{roll_counter - 1})\n")

print("✅ Setup Complete!")
print("\nTeacher Accounts:")
for config in halls_config:
    print(f"  {config['teacher']} / demo123 → {config['hall']}")

print("\nStartup:")
print("1. python app.py")
print("2. Visit http://127.0.0.1:5000/teacher/login")
print("3. Login with any teacher account above")
print("4. Select date 18.11.2025")
