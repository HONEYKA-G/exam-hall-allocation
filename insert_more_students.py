from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.Studetails
students = db.student
teachers = db.teacher

sample_date = '18.11.2025'
hall = 'ADM 303'

# Ensure teacher exists
teachers.update_one({'username':'teacher_adm303'}, {'$set':{
    'username':'teacher_adm303',
    'password':'demo123',
    'name':'Demo Teacher',
    'invigilation_hall': hall
}}, upsert=True)

# Remove previous sample students
students.delete_many({'rollnum': {'$gte': 99990000}})

cols = ['A','B','C','D','E']
benches = [1,2,3,4]
roll = 99990001
subject_cycle = ['EC19702','IT19741']
count = 0

for b in benches:
    for col in cols:
        for side in ['Left','Right']:
            if count >= 40:
                break
            subj = subject_cycle[count % len(subject_cycle)]
            seat_label = f"{col}{'L' if side=='Left' else 'R'}{b}"
            doc = {
                'rollnum': int(roll),
                'name': f'STUDENT_{roll}',
                'Year': 'FourthYear',
                'branch': 'ECE' if (count % 2 == 0) else 'IT',
                'seatnum': [
                    {
                        'date': sample_date,
                        'seatnum': seat_label,
                        'seat_label': seat_label[:2],
                        'bench_number': b,
                        'column_letter': col,
                        'side': side,
                        'classroom': hall,
                        'subject': subj
                    }
                ]
            }
            students.replace_one({'rollnum': int(roll)}, doc, upsert=True)
            roll += 1
            count += 1
    if count >= 40:
        break

print('Inserted', count, 'students for', hall, 'on', sample_date)
