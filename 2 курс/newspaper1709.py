#основные новости <div class="mp-mn-post">
#остальное <div class="d-blk-post-title">
#остальные - либо реклама, либо повтор
#Сетевое издание "Информационное агентство UlanMedia" ulanmedia.ru


import re
import urllib.request

def clean_txt(txt):
    txt = txt.replace('&quot;', '"')
    txt = txt.replace('\n', '')
    txt = txt.replace('\t', '')
    txt = txt.replace('\r', '')
    #txt = txt.replace('', '+')
    txt = re.sub('> *?<', '><', txt)
    txt = re.sub('( )+', ' ', txt)
    return txt

def extract_titles(search_pattern, txt):
    titles = re.findall(search_pattern, txt)
    print(titles)
    return titles

def main():
    '''
    url = 'http://ulanmedia.ru/'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(url, headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    '''
    url = 'http://ulanmedia.ru/'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    
    html = clean_txt(html)
    titles = extract_titles('<div class="mp-mn-post">.*?">(.*?)<', html)
    titles += extract_titles('<div class="d-blk-post-title">(?:<.*?>)?(.*?)<', html)

    output_filename = 'titles.txt'
    with open(output_filename, 'w', encoding='utf-8') as f:
        txt = '\n'.join(titles)
        txt = txt.replace('\n ', '\n')
        f.write(txt)

if __name__ == '__main__':
    main()
