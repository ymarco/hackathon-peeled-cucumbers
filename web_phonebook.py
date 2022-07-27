from bottle import route, run, template, request, redirect, response, static_file
import db
import os


@route('/add_place')
def add_restaurant_page():
    pass


@route('/add_criterion')
def add_criteion_page():
    pass


@route('/')
def main_page():
    template_dir = os.path.split(os.path.abspath(__file__))[0]
    template_name = "web_phonebook.html"
    template_file = os.path.join(template_dir, template_name)
    try:
        name = str(request.query.name)
        finds = [db.get_place_profile(0), db.get_place_profile(1), db.get_place_profile(2)]
        print(finds)
        print('requested name:', name)
    except ValueError as e:
        print('no name request')
        finds = []
    return template(template_file, finds=finds)


@route('/add_place')
def add_place():
    name, link, rating = request.query.name, request.query.link, request.query.rating
    db.add_place(name, link, rating)
    redirect("/")


if __name__ == '__main__':
    run()
