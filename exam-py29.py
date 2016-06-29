import re
import os

def task1(fn):
    f = open(fn, 'r', encoding='utf-8')
    txt = f.read()
    f.close()
    init_lastname = re.findall('(?:(?: |^)([А-ЯЁ]\. [А-ЯЁ][-А-ЯЁа-яё]+?)[.,) \n])', txt)
    for name in init_lastname:
        print(name)
    return txt

def task2(text):
    first_lastname = re.findall('(?:(?: |^)((?:[А-ЯЁ]\. )?(?:[А-ЯЁ](?:\.|[-А-ЯЁа-яё]+?)) [А-ЯЁ][-А-ЯЁа-яё]+?)[.,) \n])', text)
    for name in first_lastname:
        if re.search('[а-яё]',name):
            print(name)
    return first_lastname


def task3(names,txt):
    first_names = []
    last_names = []
    #c1 = 0
    #c2 = 0
    for name in names:
        if re.search('[а-яё]', name):
            res = re.search('^([-А-Яа-яёЁ. ]+?) ([-А-ЯЁа-яё]+?)$', name)
            last_names.append(res.group(2))
            first_names.append(res.group(1))
    for i, ln in enumerate(last_names):
        if ln not in os.listdir(path="."):
            os.makedirs(ln)
        line = '(\. |^)(([А-ЯЁ].*?)?' + first_names[i] + ' ' + last_names[i] + '.*?\.( |\n|$))'
        res = re.search(line, txt)
        #c1 += 1
        f = open(first_names[i] + ln, 'w', encoding='utf-8')
        if res:
            f.write(res.group(2))
            #print(res.group(2))
            #c2 += 1
        #else:
            #print(line)
        f.close()
    #print(c1, c2)


def main():
    file_name = 'engineer.txt'
    txt = task1(file_name)
    names = task2(txt)
    task3(names,txt)

'''
def task1():
    f = open('crypt.txt', 'r', encoding = 'utf-8')
    txt = f.read()
    cents = re.findall('(?:([IVX]+) (?:века?|в.)( до н. э.| н. э.)?)', txt)
    dts = re.findall('(?:([0-9]+) год|\(([0-9]+)\)|, ([0-9]+)\)|([0-9]+ (?:январ|феврал|март|апрел|ма|июн|июл|август|сентябр|октябр|ноябр|декабр)(?:я|ь|а|й)? [0-9]+))',txt)
    cntrs = []
    for el in cents:
        op = el[0]+el[1]
        cntrs.append(op)
        print(op)
    f.close()
    dct = {}
    for el in cntrs:
        if el in dct:
            dct[el] += 1
        else:
            dct[el] = 1
    for el in dts:
        for dt in el:
            if dt:
                if dt in dct:
                    dct[dt] += 1
                else:
                    dct[dt] = 1
    return dct


def task2(dct):
    f = open('exam-py.csv', 'w', encoding = 'utf-8')
    for el in dct:
        f.write(el+','+str(dct[el])+'\n')
    f.close()


def task3(dct):
    f = open('crypt.txt','r',encoding = 'utf-8')
    txt = f.read()
    for el in dct:
        if not re.search('[а-я]', el):
            rgx = '((?:. |\n|\t)[А-ЯЁ](?:.*)?' + el + '(?:.*)?\.)'
            line = re.findall(rgx, txt)
            if el[0] not in 'IVX':
                cntr = def_cent(el)
            else:
                cntr = el
            print(el)
            if cntr not in os.listdir('.'):
                os.makedirs(cntr)
            if cntr != el:
                dirct = './'+cntr+'/'+el+'.txt'
                fl = open (dirct,'w',encoding='utf-8')
                for i in line:
                    fl.write(i+'\n')
                fl.close()
    f.close()


def main():
    res = task1()
    task2(res)
    task3(res)
'''

if __name__ == '__main__':
    main()

