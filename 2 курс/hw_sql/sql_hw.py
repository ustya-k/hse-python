import os
import re


def get_mystem_words(filename):
    line = 'mystem.exe -nd ' + filename + ' ' + filename.replace('.txt', '_mystem.txt')
    os.system(line)
    with open(filename.replace('.txt', '_mystem.txt'), 'r', encoding='utf-8') as f:
        pairs = f.readlines()
    words_dict = {}
    max_len = 1
    for pair in pairs:
        res = re.search('(.*?){(.*?)[?}]', pair)
        word = res.group(1).lower()
        lemma = res.group(2).lower()
        if lemma in words_dict:
            words_dict[lemma] |= {word}
        else:
            words_dict[lemma] = {word}
    return words_dict


def inserts_table2(words, filename):
    id_counter = 0
    dict_of_wordforms = {}
    arr_inserts = []
    line = 'INSERT INTO table2 (id, wordform, lemma) VALUES (%d, "%s", "%s");'
    for lemma in words:
        for word in words[lemma]:
            arr_inserts.append(line % (id_counter, word, lemma))
            dict_of_wordforms[word] = id_counter
            id_counter +=1
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(arr_inserts))
    return dict_of_wordforms


def inserts_table1(wordforms, filename_in, filename_out):
    with open(filename_in, 'r', encoding = 'utf-8') as f:
        text = f.read()
    words = text.split()
    arr_inserts = []
    line = 'INSERT INTO table1 (id, token, id_table2) VALUES (%d, "%s", %d);'
    id_counter = 0
    for word in words:
        w = word.strip('.,!?:"—0123456789(/)«»')
        if w.lower() in wordforms:
            arr_inserts.append(line % (id_counter, w, wordforms[w.lower()]))
            id_counter += 1
    with open(filename_out, 'a', encoding = 'utf-8') as f:
        f.write('\n')
        f.write('\n'.join(arr_inserts))


def main():
    filename = 'sql_hw_txt.txt'
    filename2 = 'inserts.txt'
    dict_of_words = get_mystem_words(filename)
    dict_of_wordforms = inserts_table2(dict_of_words, filename2)
    inserts_table1(dict_of_wordforms, filename, filename2)
    

if __name__ == '__main__':
    main()
