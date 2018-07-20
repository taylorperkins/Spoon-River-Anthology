"""Basic Flask App
I want to be able to compare any two poems at will,
view them side by side, and compare the similarity scores
between them to determine if the scores are
indeed accurate.
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
