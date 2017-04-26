from flask import Flask
from flask import render_template, url_for, redirect, request
from urllib.parse import quote, unquote
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results')
def results():
    if request.args:
        translations = find_translations(request.args['word'])
        return render_template('results.html', url_search = url_for('index'), translations = translations, eng_word = request.args['word'])
    return redirect(url_for('index'))


def find_translations(search_word):
    with open('data/eng-thai_dictionary.json', 'r', encoding = 'utf-8') as f:
        json_txt = f.read()
    dictionary = json.loads(json_txt)
    try:
        transl = dictionary[search_word]
    except:
        transl = ['Слово не найдено']
    return transl


if __name__ == '__main__':
    app.run(debug=True)

