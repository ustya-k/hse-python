import os
import re
import html

def get_adyg_words(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        words_txt = f.read()
    words = words_txt.split()
    return words


def get_site_words(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        txt = f.read()
    regex = '<div class="abs">.*?<h1><a href=.*?>(.*?)</a>.*?<p>(.*?)</p>'
    words_arr = re.findall(regex, txt, flags = re.DOTALL)
    words = []
    for el in words_arr:
        head = el[0].split()
        snip = el[1].split()
        words += head + snip
    for i, word in enumerate(words):
        words[i] = html.unescape(word)
        words[i] = word.strip('"!.,?:;\'\\/()[]0123456789—-–­«»')
        words[i] = word.replace('I','ӏ').lower()
    ch = 0
    while ch == 0:
        try:
            words.remove('')
        except:
            ch = 1
    return set(words)


def compare_sets(wordset1, wordset2):
    common_words = wordset1 & wordset2
    return common_words

    
def task1():
    filename1 = 'adyghe-unparsed-words.txt'
    filename2 = 'adygvoice.html'
    adyg_words = get_adyg_words(filename1)
    site_words = get_site_words(filename2)
    adyg_words_set = set(adyg_words)
    common_words = compare_sets(site_words, adyg_words_set)
    with open('wordlist.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(common_words))


def get_rus_nouns(filename):
    adyg_words = get_adyg_words(filename)
    adyg_words = [word for word in adyg_words if not re.search('[ӏ0-9-]', word)] #ӏ воспринимается разделителем, слова через дефис всё равно разбираются как два, слова с числами не разбираются вообще (там есть з3) 
    filename_rus = filename.replace('.txt','_r.txt')
    with open(filename_rus, 'w', encoding='utf-8') as f:
        f.write('\n'.join(adyg_words))
    path_fin = filename_rus.replace('.txt','_mystem.txt')
    line = 'mystem.exe ' + filename_rus + ' ' + path_fin + ' -in'
    #os.system(line)
    adyg_words_morph = get_adyg_words(path_fin)
    regex = '[{|][^|}?]*?(|[^?])=[^|}]*?им[^|}]*?ед[^|}]*?[|}]'
    rus_nouns = []
    for i,word in enumerate(adyg_words):
        if re.search(regex, adyg_words_morph[i]):
            rus_nouns.append(word)
    return rus_nouns


def task2():
    filename = 'adyghe-unparsed-words.txt'
    rus_nouns = get_rus_nouns(filename)
    with open('rus_nouns.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(rus_nouns))
    return rus_nouns


def task3(words):
    filename = 'adyghe-unparsed-words_r_mystem.txt'
    words_morph = get_adyg_words(filename)
    words = set(words)
    text = ''
    line = 'INSERT INTO rus_words wordform VALUES "%s" lemma VALUES "%s"\n'
    regex = '[{|]([^|}?]*?)=[^|}]*?им[^|}]*?ед[^|}]*?[|}]'
    #regex = '[{|]([^|}?]*?)(|[^?])=[^|}]*?им[^|}]*?ед[^|}]*?[|}]'
    for w in words_morph:
        word = re.search('(.*?){',w).group(1)
        if word in words:
            lemmas = re.findall(regex, w)
            for i, lemma in enumerate(lemmas):
                lm = lemma
                if lm == '':
                    print(word)
                    ch = 0
                    t = i - 1
                    while ch == 0:
                        if lemmas[t] == '':
                            t -= 1
                        else:
                            lm = lemmas[t]
                            ch = 1
                text += line % (word, lm)      
    with open('sql.txt', 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    task1()
    rus_nouns = task2()
    task3(rus_nouns)

if __name__ == '__main__':
    main()
