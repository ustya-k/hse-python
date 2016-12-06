import re
import urllib.request
import html
from bs4 import BeautifulSoup

def get_links(url, number_of_links):
    html_page = get_html(url)
    #html_page = open_text()
    regex = 'rel="noopener" target="_blank" tabindex="0" href="(http.*?)"'
    #regex = '<a\shref="(.*?)"\sclass="j-metrics__clicks-out-source-subject article-sources__subject"'
    links = re.findall(regex, html_page, flags = re.DOTALL)
    try:
        return links[:number_of_links]
    except:
        return links


def open_text():
    with open('yandex_news.html', 'r', encoding='utf-8') as f:
        return f.read()

def get_html(link):
    req = urllib.request.Request(link)
    with urllib.request.urlopen(req) as response:
        html_page = response.read().decode('utf-8')
    return html_page

    
def number_of_cyr(text):
    res = re.findall('[А-Яа-яЁё]', text)
    return len(res)
    
    
def most_possibly_text(text):
    cr1 = number_of_cyr(text) * 0.01
    res = re.findall('[.,?!]', text)
    if cr1 < 1.5:
        cr2 = 0
    else:
        cr2 = len(res) * 1.5
    rate = cr1 + cr2
    if '©' in text or '@' in text:
        rate = 0
    elif '<' in text:
        rate /= 2
    '''    
    if rate > 10:
        print(str(cr1))
        print(str(cr2))
    '''    
    return rate
    

def get_text(html_page):
    arr_divs = get_arr_of_divs(html_page)
    return max(arr_divs, key=most_possibly_text)


def get_arr_of_divs(html_page):
    soup = BeautifulSoup(html_page, 'html.parser')
    arr_divs = soup.findAll('div')
    return [clean_block(div_block.prettify()) for div_block in arr_divs]
    

def clean_block(div_block):
    div_block = re.sub('.*?>', '', div_block, count=1)
    div_block = re.sub('<script.*?>.*?</script>', ' ', div_block, flags=re.DOTALL)
    div_block = re.sub('<div.*?>.*?</div>', ' ', div_block, flags=re.DOTALL)
    div_block = re.sub('<header>.*?</header>', ' ', div_block,flags=re.DOTALL)
    div_block = re.sub('<style.*?>.*?</style>', ' ', div_block,flags=re.DOTALL)
    div_block = div_block.replace('</div>', ' ')
    div_block = html.unescape(div_block)
    div_block = re.sub('<!--.*?-->', '', div_block, flags=re.DOTALL)
    div_block = re.sub('</?(p|a|span|ul|hr|img|h1|noscript|link|li|meta|section|iframe).*?>', '', div_block)
    tags = ['strong', 'b', 'div', 'h2', 'h3', 'em', 'ul', 'br']
    for tag in tags:
        div_block = re.sub('</?' + tag + '>', '', div_block)
    div_block = re.sub('<br/>', '', div_block)    
    div_block = re.sub('(\s)+',r'\1', div_block)
    return div_block
    

def make_a_set(text):
    arr = text.split()
    dict_of_words = {}
    for word in arr:
        w = word.strip('"!.,?:;\'\\/()[]0123456789—-–').lower()
        if w != '' and w in dict_of_words:
            dict_of_words[w] += 1
        elif w != '':
            dict_of_words[w] = 1
    return dict_of_words
    
    
def get_set_of_words(link):
    html_page = get_html(link)
    text = get_text(html_page)
    return make_a_set(text)


def sorted_text_from_set(set_of_words):    
    arr = list(set_of_words)
    arr.sort()
    text = ''
    for el in arr:
        text += el + '\n'
    return text


def get_texts(link):
        html_page = get_html(link)
        text = get_text(html_page)
        return text
    
def main():
    url = 'https://news.yandex.ru/yandsearch?lr=10743&cl4url=tass.ru%2Fekzomars-2016%2F3823717&lang=ru&rubric=science&from=index'
    #url = 'https://news.rambler.ru/europe/35494959-premer-ministr-frantsii-podal-v-otstavku/items/'
    number_of_links = 4
    links = get_links(url, number_of_links)
    #print(links)
    words_intersection = ''
    set_of_words_not_once = ''
    for link in links:
        #print(str(get_texts(link)))
        dict_of_words = get_set_of_words(link)
        set_of_words_not_once_dict = {word for word in dict_of_words if dict_of_words[word] > 1}
        set_of_words = set(dict_of_words)
        if words_intersection != '':
            words_intersection = words_intersection.intersection(set_of_words)
            part_1 = set_of_words.difference(words_union)
            #print(words_sym_difference, set_of_words)
            part_2 = words_sym_difference.difference(set_of_words)
            words_sym_difference = part_1.union(part_2)
            words_union.update(set_of_words)
        else:
            words_intersection = set_of_words
            words_union = set_of_words
            words_sym_difference = set_of_words
        if set_of_words_not_once != '':
                set_of_words_not_once.update(set_of_words_not_once_dict)
        else:
                set_of_words_not_once = set_of_words_not_once_dict
    with open('intersection.txt', 'w', encoding = 'utf-8') as f:
        f.write(sorted_text_from_set(words_intersection))
    arr_sym_dif = list(words_sym_difference)
    arr_sym_dif.sort()
    with open('symmetric_difference.txt', 'w', encoding = 'utf-8') as f:
        for word in arr_sym_dif:
                if word in set_of_words_not_once:
                        f.write(word + '\n')
    #with open('intersection.txt', 'w', encoding = 'utf-8') as f:
    #    f.write(sorted_text_from_set(words_sym_difference))

        
if __name__ == '__main__':
    main()
