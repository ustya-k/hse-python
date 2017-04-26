import os
import re
import json

def add_to_dict(text):
    search_line = '<tr><td class=th><a href=.*?>(.*?)</a>.*?<td class=pos>(.*?)</td><td>(.*?)</td></tr>'
    res = re.findall(search_line, text)
    for line in res:
        if line[1] != 'example sentence':
            eng_word = clean_eng_word(line[2])
            thai_word = clean_thai_word(line[0])
            eng_words = eng_word.split(';')
            for word in eng_words:
                if word != '':
                    if thai_word not in thai_eng_dict:
                        thai_eng_dict[thai_word] = [word]
                    else:
                        thai_eng_dict[thai_word].append(word)


def make_json(dictionary, path):
    with open(path, 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(dictionary))


def clean_eng_word(word):
    word = re.sub('<span .*?>.*?</span>', '', word)
    word = re.sub('<a.*?>.*?</a>', '', word)
    word = re.sub('</?(sub|a.*?|i|sup|u|b)>', '', word)
    word = re.sub('<br ?/?>', ' ', word)
    word = re.sub('<img.*?>', '', word)
    word = re.sub('\[.*?\]', '', word)
    word = re.sub(',.*?', '', word)
    word = re.sub('&[lg]t', '"', word)
    word = word.replace('()', '')
    word = word.replace('&#39', "'")
    word = word.replace('&#34', '"')
    word = re.sub('\\"', '"', word)
    word = re.sub(' +', ' ', word)
    word = re.sub(';+', ';', word)
    word = re.sub('^[ ;]', '', word)
    word = re.sub('; ', ';', word)
    word = re.sub('[ ;]$', '', word)
    word = re.sub(' ;', ';', word)
    return word


def clean_thai_word(word):
    word = re.sub('<img.*?>', '', word)
    word = re.sub('<br ?/?>', ' ', word)
    return word


def reverse_dict():
    eng_thai_dict = {}
    for el in thai_eng_dict:
        eng_words = thai_eng_dict[el]
        for eng_word in eng_words:
            if eng_word not in eng_thai_dict:
                eng_thai_dict[eng_word] = [el]
            else:
                eng_thai_dict[eng_word].append(el)
    return eng_thai_dict


def main():
    files = os.listdir('thai_pages')
    for file in files:
        path = 'thai_pages//' + file
        with open(path, 'r', encoding = 'utf-8') as f:
            add_to_dict(f.read())
    make_json(thai_eng_dict, 'data//thai-eng_dictionary.json')
    eng_thai_dict = reverse_dict()
    make_json(eng_thai_dict, 'data//eng-thai_dictionary.json')


if __name__ == '__main__':
    thai_eng_dict = {}
    main()
