#!/usr/bin/env python3

import sqlite3
import atexit
con = sqlite3.connect('places.db')

cur = con.cursor()
atexit.register(lambda: con.close())

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS places
               (place_id INTEGER PRIMARY KEY,
                name TEXT, google_link TEXT, rating INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS criterions
               (criterion_id INTEGER PRIMARY KEY,
                name TEXT, description TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS place_criterions
               (place_id INTEGER, criterion_id INTEGER,
                value TEXT)''')
# con.commit()

# Insert a row of data
# cur.execute("INSERT INTO places VALUES (0, 'Fabiano', 'google.com', 4)")
# cur.execute('''INSERT INTO criterions VALUES (0, 'Vegeterian', 'Percentage of non-meat dishes')''')
# cur.execute('''INSERT INTO criterions VALUES (1, 'Gluten-free', 'Percentage of gluten-free dishes')''')
# cur.execute('''INSERT INTO place_criterions VALUES (0, 1, "80%")''')

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

def search_by_name(name):
    return cur.execute("SELECT * FROM places WHERE name=?", (name,))
def get_place_profile(id):
    place = cur.execute("SELECT * FROM places WHERE place_id=?", (id,))
    try:
        place = next(place)
    except StopIteration:
        raise ValueError("Place %d does not exist" % id)
    criterions = cur.execute('''
SELECT c.name, c.description, pc.value FROM criterions c
JOIN place_criterions pc ON pc.criterion_id = c.criterion_id
    ''')
    return place, list(criterions)
print(get_place_profile(0))
