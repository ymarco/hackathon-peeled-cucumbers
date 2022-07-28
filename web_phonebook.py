from bottle import route, run, template, request, redirect
import db
import os


def search():
    try:
        name_filtered = db.search_by_name(str(request.query["name"]))
    except KeyError:
        return []

    filtered = []
    for id, name, link, rating in name_filtered:
        pc = db.get_criterions_id_for_place(id)

        add_to_filtered = True
        for x in request.query:
            if x != "name" and str(x).isnumeric():
                if all([pc[i][0] != int(x) for i in range(len(pc))]):
                    add_to_filtered = False
                    break

        if add_to_filtered:
            filtered.append(db.get_place_profile(id))

    return filtered


@route('/add_new_criterion')
def add_new_criterion():
    pass


@route('/')
def main_page():
    template_dir = os.path.split(os.path.abspath(__file__))[0]
    template_name = "web_phonebook.html"
    template_file = os.path.join(template_dir, template_name)
    try:
        name = str(request.query.name)
        finds = search()
        print('requested name:', name)
    except ValueError as e:
        print('no name request')
        finds = []
        raise e
    return template(template_file, finds=finds)


@route('/add_place')
def add_place():
    name, link, rating = request.query.name, request.query.link, request.query.rating
    db.add_place(name, link, rating)
    redirect("/")


if __name__ == '__main__':
    run(host="0.0.0.0", port=80)
