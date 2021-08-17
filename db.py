import sqlite3

db = sqlite3.connect("sqlite.db")
db.execute(open('tables.sql','r', encoding='utf-8').read())