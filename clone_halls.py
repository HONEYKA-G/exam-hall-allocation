"""
Clone students/seating from a source hall to multiple target halls.
Generates new roll numbers in a fresh range to avoid collisions and creates teacher accounts.
"""
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.Studetails
students = db.student
teachers = db.teacher

source_hall = 'ADM 303'
sample_date = '18.11.2025'
# target halls to create (example from your image)
target_halls = ['B212', 'B213', 'B218', 'B219']

# Starting roll for cloned students (choose a range unlikely to collide with existing)
start_roll_base = 98000001

print(f"Cloning students from {source_hall} (date={sample_date}) to: {', '.join(target_halls)}")

# Fetch source students for the date
src_students = list(students.find({'seatnum.classroom': source_hall}))
# Filter to those having the specific date and pick the matching seat entry
src_filtered = []
for s in src_students:
    for seat in s.get('seatnum', []) or []:
        if isinstance(seat, dict) and seat.get('date') == sample_date:
            student_copy = dict(s)
            # attach the matched seat as primary
            student_copy['_orig_seat'] = seat
            src_filtered.append(student_copy)
            break

print(f"Found {len(src_filtered)} source students to clone.")

roll_counter = start_roll_base
for hall in target_halls:
    # Create teacher for this hall
    username = f"teacher_{hall.replace(' ', '').lower()}"
    teachers.update_one({'username': username}, {'$set':{
        'username': username,
        'password': 'demo123',
        'name': f'Teacher {hall}',
        'invigilation_hall': hall
    }}, upsert=True)
    print(f"Created/updated teacher: {username} -> {hall}")

    # Insert cloned students for this hall; keep same seating positions but classroom replaced
    count = 0
    for s in src_filtered:
        orig_seat = s.get('_orig_seat', {})
        new_roll = roll_counter
        roll_counter += 1

        # build new student doc
        new_doc = {
            'rollnum': int(new_roll),
            'name': s.get('name') + f"_{hall}",
            'Year': s.get('Year', 'FourthYear'),
            'branch': s.get('branch', s.get('department', '')),
            'department': s.get('department', ''),
            'seatnum': [
                {
                    'date': sample_date,
                    'seatnum': orig_seat.get('seatnum'),
                    'seat_label': orig_seat.get('seat_label'),
                    'bench_number': orig_seat.get('bench_number'),
                    'column_letter': orig_seat.get('column_letter'),
                    'side': orig_seat.get('side'),
                    'classroom': hall,
                    'subject': orig_seat.get('subject')
                }
            ]
        }
        students.replace_one({'rollnum': int(new_roll)}, new_doc, upsert=True)
        count += 1
    print(f"  ✓ Inserted {count} cloned students into {hall} (rolls {start_roll_base}-{roll_counter-1})")

print('\nClone complete.\n')
print('Notes:')
print('- New teachers created with password demo123.')
print('- New cloned students have roll numbers starting at', start_roll_base)
print("- Start the Flask app and login with teacher_<hall> accounts to verify each hall.")
