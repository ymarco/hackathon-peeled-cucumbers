import collections
from bottle import route, run, template, request, redirect, response, static_file
import json
import csv
import re
import os

def load_phones(filename):
    with open(filename) as csvfile:
        table = csv.reader(csvfile)
        return [(name.strip(), phone.strip()) for name, phone in table]

def search(search_name, search_phone, phone_table):
    if not search_name and search_phone:
        search_phone = search_phone.strip().translate({'-': None})
        res = [(n, p) for n, p in phone_table if p.startswith(search_phone)]
        return res
    if not search_phone and search_name:
        p_s = ".*(" + search_name + r").*"
        try:
            p = re.compile(p_s)
        except Exception:
            print('invalid name:', search_name,
                ', which created the pattern', p_s)
            return []

        matches = (p.match(name) for name, _ in phone_table)
        print('matches:', matches)
        res = []
        for info, match in zip(phone_table, matches):
            if match:
                res.append(info)
        return res
    return []


@route('/')
def index():
    return template("""
        <html>
        <body>
        Hello - welcome to your web-server
        </body>
        </html>
        """)

@route('/add_place')
def add_restaurant_page():
    pass

@route('/add_criterion')
def add_criteion_page():
    pass

@route('/foollergy')
def main_page():
    template_dir = os.path.split(os.path.abspath(__file__))[0]
    template_name = "web_phonebook.html"
    template_file = os.path.join(template_dir, template_name)
    try:
        name = str(request.query.name)
        phone = str(request.query.phone)
        finds = search(name, phone, phone_table)
        finds = [("OdyMisada", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 4.5, [("Vegan", "ONLY MEAT", 5)])]
        print('requested name:', name)
    except ValueError as e:
        print('no name request')
        finds = []
    return template(template_file, finds=finds)

if __name__ == '__main__':
    phone_table = load_phones('.\phones.csv')
    print(phone_table)
    run()
