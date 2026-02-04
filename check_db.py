from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client.Studetails

print('Teachers in DB:')
for t in db.teacher.find():
    print('-', t.get('username'), '|', t.get('name'), '| hall=', t.get('invigilation_hall'))

print('\nSample students (roll >= 99990000):')
for s in db.student.find({'rollnum': {'$gte': 99990000}}):
    print('-', s.get('rollnum'), s.get('name'))
    for seat in s.get('seatnum', []) or []:
        print('   ', seat.get('date'), seat.get('seatnum'), seat.get('column_letter'), seat.get('bench_number'), seat.get('side'), seat.get('classroom'), seat.get('subject'))

print('\nTotal teachers:', db.teacher.count_documents({}))
print('Total sample students:', db.student.count_documents({'rollnum': {'$gte': 99990000}}))
