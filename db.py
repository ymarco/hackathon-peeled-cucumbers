#!/usr/bin/env python3

import sqlite3
import atexit

con = sqlite3.connect('places.db')

cur = con.cursor()
atexit.register(lambda: con.close())

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS places
               (place_id INTEGER PRIMARY KEY,
                name TEXT, link TEXT, rating INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS criterions
               (criterion_id INTEGER PRIMARY KEY,
                name TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS place_criterions
               (place_id INTEGER, criterion_id INTEGER, description TEXT,
                value TEXT)''')
# con.commit()

# Insert a row of data
# cur.execute("INSERT INTO places VALUES (0, 'Fabiano', 'google.com', 4)")
# cur.execute('''INSERT INTO criterions VALUES (0, 'Vegeterian')''')
# cur.execute('''INSERT INTO criterions VALUES (1, 'Gluten-free')''')
# cur.execute('''INSERT INTO place_criterions VALUES (0, 1, 'Percentage of gluten-free dishes', "80%")''')

# Save (commit) the changes
con.commit()
max_places_id = next(cur.execute("SELECT MAX(place_id) FROM places"))[0]
max_criterion_id = next(cur.execute("SELECT MAX(criterion_id) FROM criterions"))[0]


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
SELECT c.name, pc.description, pc.value FROM criterions c
JOIN place_criterions pc ON pc.criterion_id = c.criterion_id
    ''')
    return place[1], place[2], place[3], list(criterions)


def add_place(name, link, rating):
    global max_places_id
    max_places_id += 1
    cur.execute("INSERT INTO places VALUES (?, ?, ?, ?)", (max_places_id,
                                                           name, link, rating))
    con.commit()


def remove_place(id):
    cur.execute("DELETE FROM places WHERE place_id=?", (id,))
    con.commit()


def add_criterion(name, description):
    global max_criterion_id
    max_criterion_id += 1
    cur.execute("INSERT INTO criterions VALUES (?, ?, ?)", (max_criterion_id,
                                                            name, description))
    con.commit()


def remove_criterion(id):
    cur.execute("DELETE FROM criterions WHERE place_id=?", (id,))
    con.commit()


def add_place_criterion(place_id, criterion_id, value):
    cur.execute("INSERT INTO place_criterions VALUES (?, ?, ?)", (place_id,
                                                                  criterion_id, value))
    con.commit()
