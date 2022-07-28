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
               (place_id INTEGER, criterion_id INTEGER, description TEXT)''')
# con.commit()

# Save (commit) the changes
con.commit()
max_places_id = next(cur.execute("SELECT MAX(place_id) FROM places"))[0]
if max_places_id is None: max_places_id = 0
max_criterion_id = next(cur.execute("SELECT MAX(criterion_id) FROM criterions"))[0]
if max_criterion_id is None: max_criterion_id = 0


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

def search_by_name(name):
    return cur.execute("SELECT * FROM places WHERE name LIKE '{}%'".format(name))


def get_place_profile(id):
    place = cur.execute("SELECT * FROM places WHERE place_id=?", (id,))
    try:
        place = next(place)
    except StopIteration:
        raise ValueError("Place %d does not exist" % id)
    criterions = cur.execute('''
SELECT c.name, pc.description FROM criterions c
JOIN place_criterions pc ON pc.criterion_id = c.criterion_id AND pc.place_id=?
    ''', (id,))
    return place[1], place[2], place[3], list(criterions)


def get_criterions_id_for_place(place_id):
    criterions_ids = cur.execute('''
    SELECT pc.criterion_id FROM criterions c
    JOIN place_criterions pc ON pc.criterion_id = c.criterion_id AND pc.place_id=?
        ''', (place_id,))

    return list(criterions_ids)


def add_place(name, link, rating):
    global max_places_id
    max_places_id += 1
    cur.execute("INSERT INTO places VALUES (?, ?, ?, ?)", (max_places_id,
                                                           name, link, rating))
    con.commit()

    return max_places_id


def remove_place(id):
    cur.execute("DELETE FROM places WHERE place_id=?", (id,))
    con.commit()


def add_criterion(name):
    global max_criterion_id
    max_criterion_id += 1
    cur.execute("INSERT INTO criterions VALUES (?, ?)", (max_criterion_id,
                                                         name))
    con.commit()

    return max_criterion_id


def remove_criterion(id):
    cur.execute("DELETE FROM criterions WHERE place_id=?", (id,))
    con.commit()


def add_place_criterion(place_id, criterion_id, description):
    cur.execute("INSERT INTO place_criterions VALUES (?, ?, ?)", (place_id,
                                                                  criterion_id, description))
    con.commit()


def remove_place_criterion(place_id, criterion_id):
    cur.execute('DELETE FROM place_criterions WHERE place_id=? AND criterion_id=?', (place_id,
                                                                                     criterion_id))
    con.commit()


def update_place_criterion_description(place_id, criterion_id, new_description):
    remove_place_criterion(place_id, criterion_id)
    add_place_criterion(place_id, criterion_id, new_description)


def get(x):
    cur.execute(f"SELECT * FROM {x}")
    print(cur.fetchall())
    con.commit()


get("places")
get("place_criterions")
get("criterions")

a = False
b = True

if __name__ == "__main__" and a:
    cur.execute("INSERT INTO places VALUES (0, 'Fabiano', 'https://google.com/', 4)")
    cur.execute('''INSERT INTO criterions VALUES (0, 'Vegeterian')''')
    cur.execute('''INSERT INTO criterions VALUES (1, 'Gluten-free')''')
    cur.execute('''INSERT INTO criterions VALUES (2, 'Lactose-free')''')
    cur.execute('''INSERT INTO criterions VALUES (3, 'Eggs')''')
    cur.execute('''INSERT INTO criterions VALUES (4, 'Vegan')''')
    cur.execute('''INSERT INTO criterions VALUES (5, 'Nuts')''')
    cur.execute('''INSERT INTO criterions VALUES (6, 'High-Protein')''')
    cur.execute('''INSERT INTO criterions VALUES (7, 'Crohn')''')
    cur.execute('''INSERT INTO criterions VALUES (8, 'Sesame')''')
    cur.execute('''INSERT INTO place_criterions VALUES (0, 1, 'Percentage of gluten-free dishes - 80%')''')

    i = add_place("McDonald's", "https://www.mcdonalds.co.il/", 3.5)
    add_place_criterion(i, 0, """
    green salad -
    Fresh green salad with walnuts and a sauce of your choice ------- 30₪
    """)

    get("place_criterions")
    get("criterions")
    get("places")

if __name__ == "__main__" and b:
    remove_place(2)
    i = add_place("Vegan Restaurant 1", "https://www.youtube.com/watch?v=OzcgM0U51m4", 4.9)
    """"add_place_criterion(2, 0, "Everything that is vegan is vegetarian.")
    add_place_criterion(2, 3, "No eggs in everything.")
    add_place_criterion(2, 4, "Everything is Vegan.")
    add_place_criterion(2, 8, "Most meals contain sesame. It is possible to prepare those meals sesame-free.")"""


    get("place_criterions")
    get("criterions")
    get("places")
