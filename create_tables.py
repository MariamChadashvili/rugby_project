import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT, email TEXT, mobile_number TEXT, password TEXT)')
print("Created users table successfully!")

conn.execute('CREATE TABLE teams (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, player_num INTEGER, address TEXT, rank TEXT, creator_id INTEGER, FOREIGN KEY (creator_id) REFERENCES users (id))')
print("Created teams table successfully!")

conn.execute('CREATE TABLE team_members (id INTEGER PRIMARY KEY AUTOINCREMENT, player_id INTEGER, team_id INTEGER, FOREIGN KEY (player_id) REFERENCES users (id), FOREIGN KEY (team_id) REFERENCES teams (id))')
print("Created team_members table successfully!")

conn.close()
