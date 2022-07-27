import collections
from bottle import route, run, template, request, redirect, response, static_file
import json
import csv
import re
import os

@route('/')
def phones_page():
    template_dir = os.path.split(os.path.abspath(__file__))[0]
    template_name = "web_phonebook.html"
    template_file = os.path.join(template_dir, template_name)
    try:
        name = str(request.query.name)
        phone = str(request.query.phone)
        finds = [("OdyMisada", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 4.5, [("Vegan", "ONLY MEAT", 5)])]
        print('requested name:', name)
    except ValueError as e:
        print('no name request')
        finds = []
    return template(template_file, finds=finds)

if __name__ == '__main__':
    run()
