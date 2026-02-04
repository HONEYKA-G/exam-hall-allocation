"""
Setup teachers with unique Teacher IDs and standardized credentials.
Each teacher logs in with:
  - Username: T001, T002, T003, ..., T008 (Teacher ID)
  - Password: pass123 (same for all)
  - Display Name: Teacher <HallName> (without any room/hall string duplicates)
"""

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.Studetails
teachers = db.teacher

# Define all 8 halls with their Teacher IDs
teachers_config = [
    {
        'teacher_id': 'T001',
        'hall': 'ADM 303',
        'display_name': 'Teacher ADM303'
    },
    {
        'teacher_id': 'T002',
        'hall': 'ADM 304',
        'display_name': 'Teacher ADM304'
    },
    {
        'teacher_id': 'T003',
        'hall': 'ADM 305',
        'display_name': 'Teacher ADM305'
    },
    {
        'teacher_id': 'T004',
        'hall': 'ADM 306',
        'display_name': 'Teacher ADM306'
    },
    {
        'teacher_id': 'T005',
        'hall': 'B212',
        'display_name': 'Teacher B212'
    },
    {
        'teacher_id': 'T006',
        'hall': 'B213',
        'display_name': 'Teacher B213'
    },
    {
        'teacher_id': 'T007',
        'hall': 'B218',
        'display_name': 'Teacher B218'
    },
    {
        'teacher_id': 'T008',
        'hall': 'B219',
        'display_name': 'Teacher B219'
    },
]

# Clear existing teachers and recreate with new credentials
teachers.delete_many({})

print("Setting up teachers with Teacher IDs and standardized credentials...\n")
print("=" * 70)
print(f"{'Teacher ID':<15} {'Hall':<15} {'Display Name':<25} {'Password':<15}")
print("=" * 70)

for teacher_config in teachers_config:
    teacher_id = teacher_config['teacher_id']
    hall = teacher_config['hall']
    display_name = teacher_config['display_name']
    password = 'pass123'
    
    # Create/update teacher in database
    teachers.update_one(
        {'username': teacher_id},
        {
            '$set': {
                'username': teacher_id,
                'password': password,
                'name': display_name,
                'invigilation_hall': hall
            }
        },
        upsert=True
    )
    
    print(f"{teacher_id:<15} {hall:<15} {display_name:<25} {password:<15}")

print("=" * 70)
print("\n✓ All teachers setup complete!\n")
print("Login credentials for all teachers:")
print(f"  Username: T001 to T008 (Teacher ID)")
print(f"  Password: pass123 (same for all)")
print(f"\nEach teacher is assigned to their respective hall.")
