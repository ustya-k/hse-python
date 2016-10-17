import re
import os
import urllib.request

checked_links = []

def mystem_txt(path_orig):
    path_fin = path_orig.replace('plain', 'mystem-plain')
    print('hey')
    line = 'C:\\ulanmedia\\mystem.exe ' + path_orig + ' ' + path_fin + ' -cid'
    os.system(line)

def mystem_xml(path_orig):
    path_fin = path_orig.replace('plain', 'mystem-xml')
    path_fin = path_fin.replace('txt', 'xml')
    path_fin_dirs = re.sub('article\d*?\.xml', '', path_fin)
    if not os.path.exists(path_fin_dirs):
        os.makedirs(path_fin_dirs)
    line = 'C:\\ulanmedia\\mystem.exe ' + path_orig + ' ' + path_fin + ' -cid --format xml'
    os.system(line)

def add_meta(au, ti, da, topic, url, html):
    meta_d = '@au %s\n@ti %s\n@da %s\n@topic %s\n@url %s\n' % (au, ti, da, topic, url)
    html = meta_d + html
    return html

def clean_the_html(html):
    text_re = re.search('<div class="page-content">(?:<p><b>(?:.*?)</b>)?((.|\s)*?)<div class="(?:f-)?comment-box">', html)
    text = text_re.group(1)
    replace_symbols = {'&mdash;':'—', '&ndash;':'–', '&#1257;':'ө', '&#1199;':'ү', '&#1256;':'Ө', '&#1198;':'Ү', '&#1210;':'Һ', '&#1211;':'һ', '&hellip;':'…', '&quot;':'"'}
    for sym in replace_symbols:
        text = text.replace(sym, replace_symbols[sym])
    text = re.sub('</?(p|a).*?>', '', text)
    text = re.sub('<div(.|\s)*?</div>', '', text)
    text = re.sub('\(Подробнее здесь.*?\)', '', text)
    text = re.sub('<strong>С?СЫЛКИ ПО ТЕМЕ:(.|\s)*', '', text)
    tags = ['strong', 'b', 'div', 'h2', 'h3', 'em', 'ul', 'li']
    for tag in tags:
        text = re.sub('</?' + tag + '>', '', text)
    text = re.sub('(\s)+',r'\1', text)
    return text

def get_html(link):
    req = urllib.request.Request(link)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    return html


def use_html(html):
    #1 - year 2 - month 3 - date
    meta_url = re.search('og:url" content="(.*?([0-3][0-9]\.([0-1][0-9])\.(20[0-1][0-9])).*?)"', html)
    #print(html[:100])
    date_with_dots = meta_url.group(2)
    url = meta_url.group(1)
    month = meta_url.group(3)
    year = meta_url.group(4)
    meta_title = re.search('og:title" content="(.*?)"', html)
    meta_topic = re.search('sections:\'(.*?)\'', html)
    author = 'Noname'
    title = meta_title.group(1)
    if meta_topic:
        topic = meta_topic.group(1)
    else:
        topic = ''
    meta_line = '%s\t\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tреспубликанская\t%s\tUlanMedia\t\t%s\tгазета\tРоссия\tБурятия\tru'
    #check existance of folders
    file_path = '.\\plain\\%s\\%s' % (year, month)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    #add file
    article_number = len(os.listdir(file_path)) + 1
    text = clean_the_html(html)

    article_path = file_path + '\\article' + str(article_number) + '.txt' 
    article = open(article_path, 'w', encoding = 'utf-8')
    #print(article_path)
    article.write(text)
    article.close()
    
    article_path_mystem_txt = file_path.replace('plain', 'mystem-plain')
    print('0')
    if not os.path.exists(article_path_mystem_txt):
        os.makedirs(article_path_mystem_txt)
    print('1')
    article_path_mystem_txt = article_path.replace('plain', 'mystem-plain')
    print('2')
    mystem_xml(article_path)
    mystem_txt(article_path)
    print('3')
    
    text = add_meta(author, title, date_with_dots, topic, url, text)
    #table
    
    article = open(article_path, 'w', encoding = 'utf-8')
    #print(article_path)
    article.write(text)
    article.close()
    
def crawl(depth, crawled_page):
    search_line = '<a href="(http://ulanmedia.ru/.*?\.html)"'
    links_on_page = re.findall(search_line, crawled_page)
    for link in links_on_page:
        if link not in checked_links:
            try:
                html_page = get_html(link)
                use_html(html_page)
                #print(link, depth)
                checked_links.append(link)
                if depth != 0:
                    crawl(depth - 1, html_page)
            except:
                checked_links.append(link)
                
def main():
    meta_table = open('metadata.csv', 'a', encoding = 'utf-8')
    url = 'http://ulanmedia.ru/'
    main_page = get_html(url)
    checked_links.append(url)
    crawl(0, main_page)
    #print(checked_links)


if __name__ == '__main__':
    main()
