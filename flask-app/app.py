import pickle

from flask import Flask, render_template, url_for

from utils import convert_poem_to_html
from logic.create_network_graph import create_network_graph


app = Flask(__name__)

n_largest = pickle.load(open('../notebooks/pivot/n_largest.p', 'rb'))
poem_names = pickle.load(open('../notebooks/pivot/chapter_names.p', 'rb'))

n_largest_with_names = dict()
for key_ind, scores in n_largest.items():
    n_largest_with_names[key_ind] = {'name': poem_names[key_ind]}

    for score, ind in scores:
        n_largest_with_names[key_ind][str(ind)] = (score, poem_names[str(ind)])


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<p1>/<p2>')
def compare_poems(p1, p2):
    min_poem = min([int(p1), int(p2)])
    max_poem = max([int(p1), int(p2)])

    create_network_graph(min_poem, max_poem)

    return render_template(
        'index.html',
        score=round(n_largest_with_names[p1][p2][0], 3),
        p1_name=n_largest_with_names[p1]['name'],
        p2_name=n_largest_with_names[p1][p2][1],
        p1_html=convert_poem_to_html(int(p1) + 1),
        p2_html=convert_poem_to_html(int(p2) + 1),
        poem_names=n_largest_with_names,
        poem_image="<img id=" + '-'.join([str(min_poem), str(max_poem)]) + " class='rounded mx-auto d-block' alt='...' src=" + url_for('static', filename=f'images/{min_poem}_{max_poem}_network_graph.png') + ">"
    )


if __name__ == '__main__':
    app.run()
