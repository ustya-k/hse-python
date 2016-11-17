from flask import Flask
from flask import render_template, url_for, redirect, request
from urllib.parse import quote, unquote
import json

app = Flask(__name__)

@app.route('/')
def index():
    if request.args:
        if request.args['language']:
            create_table(request.args)
        return redirect(url_for('thanks'))
    return render_template('main.html', search=url_for('search'), names=names, url_json=url_for('json_file'), url_table=url_for('stats'))

@app.route('/thanks')
def thanks():
    return render_template('thanks.html', url=url_for('index'))

@app.route('/search')
def search():
    return render_template('search.html', url=url_for('index'), names=names)

@app.route('/results')
def results():
    if request.args:
        lang_transl = make_dictionary_language_translation(request.args['answer'])
        return render_template('results.html', url_home=url_for('index'), lang_transl=lang_transl, url_search=url_for('search'))
    return redirect(url_for('search'))


@app.route('/json')
def json_file():
    return render_template('answers.json')


@app.route('/stats')
def stats():
    tags = ['age','language','bilingual','second_language']
    tags += names
    table = get_table()
    return render_template('stats.html', names=names, tags=tags, data=table, url_home=url_for('index'))


def create_table(answers):
    with open('templates/answers.json', 'r', encoding = 'utf-8') as f:
        json_txt = f.read()
    json_str = json.dumps(answers)
    with open('templates/answers.json', 'w', encoding = 'utf-8') as f:
        f.write(json_txt[:-1] + json_str + ',]')


def get_table():
    with open('templates/answers.json', 'r', encoding = 'utf-8') as f:
        json_txt = f.read()
    json_table = json.loads(json_txt)
    return json_table


def make_dictionary_language_translation(action_name):
    lang_transl = {}
    with open('templates/answers.json', 'r', encoding = 'utf-8') as f:
        json_txt = f.read()
    dicts = json.loads(json_txt)
    for dictionary in dicts:
        lang = unquote(dictionary['language'])
        try:
            gest = unquote(dictionary[action_name])
            if lang not in lang_transl:
                lang_transl[lang] = [gest]
            else:
                lang_transl[lang].append(gest)
        except:
            print('no answer for ' + lang)
    return lang_transl


if __name__ == '__main__':
    names = ['crossed_legs','crossed_legs_down','on_toes','spread_legs','swing_leg']
    app.run(debug=True)
