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


def task3(names,txt,fn):
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
        line = '(\. |^)(([А-ЯЁ].*?)?' + first_names[i] + ' ' + last_names[i] + '.*?(\.|;)( |\n|$))'
        res = re.search(line, txt)
        #c1 += 1
        f = open(first_names[i] + ln, 'w', encoding='utf-8')
        if res:
            f.write(res.group(2))
            #print(res.group(2))
            #c2 += 1
        else:
            fl = open(fn, 'r', encoding='utf-8')
            lines = fl.readlines()
            fl.close()
            for line in lines:
                ch = first_names[i] + ' ' + ln
                if ch in line:
                    f.write(line)
        f.close()
    #print(c1, c2)


def main():
    file_name = 'engineer.txt'
    txt = task1(file_name)
    names = task2(txt)
    task3(names, txt, file_name)
    #res = re.search('Михаила Архангела, покровителя дома Романовых, и причуде Павла I, принявшего титул Великого магистра Мальтийского ордена, называть все свои дворцы «замками»',txt)
    #print(res)

if __name__ == '__main__':
    main()

