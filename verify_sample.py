from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client.Studetails
stucollections = db.student

hall = 'ADM 303'
date = '18.11.2025'

students = list(stucollections.find({'seatnum.classroom': hall}))
print(f'Found {len(students)} students in hall {hall}')
for s in students:
    print('---')
    print('rollnum:', s.get('rollnum'))
    print('name:', s.get('name'))
    for seat in s.get('seatnum', []):
        print('  date:', seat.get('date'), 'seat:', seat.get('seatnum'), 'col:', seat.get('column_letter'), 'bench:', seat.get('bench_number'), 'side:', seat.get('side'), 'subject:', seat.get('subject'))
