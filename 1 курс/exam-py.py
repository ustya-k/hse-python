import re
import os

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


def def_cent(year):
    year = int(year)
    cntr = year / 100
    cntr = int(cntr)
    if cntr == 1:
        return 'I'
    if cntr == 2:
        return 'II'
    if cntr == 3:
        return 'III'
    if cntr == 4:
        return 'IV'
    if cntr == 5:
        return 'V'
    if cntr == 6:
        return 'VI'
    if cntr == 7:
        return 'VII'
    if cntr == 8:
        return 'VIII'
    if cntr == 9:
        return 'IX'
    if cntr == 10:
        return 'X'
    if cntr == 11:
        return 'XI'
    if cntr == 12:
        return 'XII'
    if cntr == 13:
        return 'XIII'
    if cntr == 14:
        return 'XIV'
    if cntr == 15:
        return 'XV'
    if cntr == 16:
        return 'XVI'
    if cntr == 17:
        return 'XVII'
    if cntr == 18:
        return 'XVIII'
    if cntr == 19:
        return 'XIX'
    if cntr == 20:
        return 'XX'
    if cntr == 21:
        return 'XXI'



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

if __name__ == '__main__':
    main()