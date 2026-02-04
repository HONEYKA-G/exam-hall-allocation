from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.Studetails
teachers = db.teacher
students = db.student

sample_date = '18.11.2025'
hall = 'ADM 303'

# Insert/update teacher
teachers.update_one({'username':'teacher_adm303'}, {'$set':{
    'username':'teacher_adm303',
    'password':'demo123',
    'name':'Demo Teacher',
    'invigilation_hall': hall
}}, upsert=True)

# Remove previous sample students with roll >= 99990000
students.delete_many({'rollnum': {'$gte': 99990000}})

sample_students = [
    (99990001, 'STUDENT A', 'FourthYear', 'A', 1, 'Left', 'EC19702'),
    (99990002, 'STUDENT B', 'FourthYear', 'A', 1, 'Right', 'EC19702'),
    (99990003, 'STUDENT C', 'FourthYear', 'B', 1, 'Left', 'IT19741'),
    (99990004, 'STUDENT D', 'FourthYear', 'B', 1, 'Right', 'IT19741'),
    (99990005, 'STUDENT E', 'FourthYear', 'A', 2, 'Left', 'EC19702'),
    (99990006, 'STUDENT F', 'FourthYear', 'A', 2, 'Right', 'EC19702'),
]

for roll, name, year, col, bench, side, subj in sample_students:
    seat_label = f"{col}{'L' if side=='Left' else 'R'}{bench}"
    doc = {
        'rollnum': int(roll),
        'name': name,
        'Year': year,
        'branch': 'ECE',
        'seatnum': [
            {
                'date': sample_date,
                'seatnum': seat_label,
                'seat_label': seat_label[:2],
                'bench_number': bench,
                'column_letter': col,
                'side': side,
                'classroom': hall,
                'subject': subj
            }
        ]
    }
    students.replace_one({'rollnum': int(roll)}, doc, upsert=True)

print('Inserted teacher and', len(sample_students), 'students for', hall, 'on', sample_date)
