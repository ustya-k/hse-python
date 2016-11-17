import os
import re


def transliterate(string):
    letters = {u'А': u'A',
               u'Б': u'B',
               u'В': u'V',
               u'Г': u'G',
               u'Д': u'D',
               u'Е': u'E',
               u'Ё': u'E',
               u'Ж': u'ZH',
               u'З': u'Z',
               u'И': u'I',
               u'Й': u'J',
               u'К': u'K',
               u'Л': u'L',
               u'М': u'M',
               u'Н': u'N',
               u'О': u'O',
               u'П': u'P',
               u'Р': u'R',
               u'С': u'S',
               u'Т': u'T',
               u'У': u'U',
               u'Ф': u'F',
               u'Х': u'H',
               u'Ц': u'TS',
               u'Ч': u'CH',
               u'Ш': u'SH',
               u'Щ': u'SCH',
               u'Ъ': u'',
               u'Ы': u'Y',
               u'Ь': u'',
               u'Э': u'E',
               u'Ю': u'JU',
               u'Я': u'JA',
               u'а': u'a',
               u'б': u'b',
               u'в': u'v',
               u'г': u'g',
               u'д': u'd',
               u'е': u'e',
               u'ё': u'e',
               u'ж': u'zh',
               u'з': u'z',
               u'и': u'i',
               u'й': u'j',
               u'к': u'k',
               u'л': u'l',
               u'м': u'm',
               u'н': u'n',
               u'о': u'o',
               u'п': u'p',
               u'р': u'r',
               u'с': u's',
               u'т': u't',
               u'у': u'u',
               u'ф': u'f',
               u'х': u'h',
               u'ц': u'ts',
               u'ч': u'ch',
               u'ш': u'sh',
               u'щ': u'sch',
               u'ъ': u'',
               u'ы': u'y',
               u'ь': u'',
               u'э': u'e',
               u'ю': u'ju',
               u'я': u'ja',
               u'ѣ': u'e',
               u'Ѣ': u'e',
               u'Ҍ': u'e',
               u'ҍ': u'e',
               u'і': u'i'}

    for cyrillic_string, latin_string in letters.items():
        string = string.replace(cyrillic_string, latin_string)

    return string


def create_directories(first_number, last_number, path):
    i = first_number
    while i <= last_number:
        if not os.path.exists(path + str(i)):
            os.makedirs(path + str(i))
        i += 1


def clean_the_text(original_text):
    changed_text = re.sub('</?div.*?>(\n|$)', '', original_text) #удаление div
    changed_text = re.sub('<h([0-9]).*?>', r'<p class="h\1">', changed_text)
    changed_text = re.sub('</h([0-9]*?)>', '</p>', changed_text)
    changed_text = re.sub('<a(.|\n)*?type="note".*?</a>', '', changed_text)
    changed_text = re.sub('<sup>.*?</sup>', '', changed_text)
    changed_text = re.sub('<span class="[on]pnumber">.*?</span>', '', changed_text)
    changed_text = re.sub('<p.*?(НЕОПУБЛИКОВАННОЕ, НЕОТДЕЛАННОЕ И НЕОКОНЧЕННОЕ|ПРИМЕЧАНИЯ|ПРОИЗВЕДЕНИЯ|СТАТЬИ|ВАРИАНТЫ|АВТОБИОГРАФИЧЕСКИЕ ЗАПИСИ|ДНЕВНИК).*?/p>\n', '', changed_text)
    changed_text = re.sub('\n+', '\n', changed_text) #удаление пустых строк
    return changed_text


def change_format(file_name):
    return file_name.replace('xhtml', 'xml')


def escape_character(original_line):
    new_line = re.sub('\\[', '\[', original_line)
    new_line = re.sub('\\]', '\]', new_line)
    new_line = re.sub('\\(', '\(', new_line)
    new_line = re.sub('\\)', '\)', new_line)
    new_line = re.sub('\\+', '\+', new_line)
    new_line = re.sub('\\?', '\?', new_line)
    return new_line


def add_line(line, transliterated_filename, filename):
    new_line = filename + ',' + change_format(transliterated_filename) + line[len(filename):]
    if not re.search('\r|\n', new_line[-1]):
        new_line += '\n'
    return new_line


def compile_head(line_with_metadata, lat_filename, search_name):
    head = '<?xml version="1.0" encoding="utf-8"?><html><head>'
    head += add_tags(line_with_metadata, search_name, lat_filename)
    head += '</head>\n<body>\n'
    return head


def compile_metaline(tag_name, tag_content):
    return '\n<meta content="' + tag_content + '" name="' + tag_name + '"></meta>'


def add_tags(line_with_metadata, search_name, lat_filename):
    search_line = search_name + ',(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?),(".*?"|«.*?»|.*?)$'
    search_results = re.search(search_line, line_with_metadata)
    #1 - value, 2 - ???, 3 - ???, 4 - author, 5 - name, 6 - sub_name (without a tag), 7 - date, 8 - place,
    #9 - time, 10 - sphere, 11 - type, 12 - topic, 13 - dop, 14 - cycle, 15 - finished,
    #16 - edited, 17 - fin/ver, 18 - orpho, 19 - source
    tagged_text = ''
    tagged_text += compile_metaline('filename2', change_format(lat_filename))
    tagged_text += compile_metaline('value', search_results.group(1))
    tagged_text += compile_metaline('author', search_results.group(4).strip('"'))
    complete_filename = search_results.group(5) + ' ' + search_results.group(6)
    tagged_text += compile_metaline('name', complete_filename.strip('"'))
    tag_names = ['date', 'place', 'time', 'sphere', 'type', 'topic', 'dop', 'cycle', 'finished', 'edited', 'fin/ver', 'orpho', 'source']
    i = 7
    for tag in tag_names:
        tagged_text += compile_metaline(tag, search_results.group(i).strip('"'))
        i += 1
    return tagged_text

def main():
    path_to_original_volumes = 'test_volumes'
    new_table = ''
    with open('test_volumes\\test_volumes_table.csv', 'r', encoding = 'utf-8') as original_table_file:
        original_table = original_table_file.readlines()
    path_to_new_volumes = 'test_volumes_output' + os.sep
    create_directories(1, 4, path_to_new_volumes)
    for root, dirs, files in os.walk(path_to_original_volumes):
        for volume in dirs:
            path_to_the_volume = root + os.sep + volume
            for r, d, f in os.walk(path_to_the_volume):
                for filename in f:
                    path_to_the_original_file = path_to_the_volume+ os.sep + filename
                    with open(path_to_the_original_file, 'r', encoding = 'utf-8') as original_file:
                        original_text = original_file.read()
                    
                    transliterated_filename = transliterate(filename)
                    correct_for_search_line = escape_character(filename)
                    for line in original_table:
                        if re.search('^' + correct_for_search_line + ',' + volume + ',.*?$', line):
                            head = compile_head(line, transliterated_filename, correct_for_search_line)
                            new_table += add_line(line, transliterated_filename,filename)
                            break
                    new_text = head + clean_the_text(original_text) + '\n</body></html>'
                    path_to_the_new_file = path_to_the_volume.replace('test_volumes','test_volumes_output') + os.sep + change_format(transliterated_filename) #новый файл
                    with open(path_to_the_new_file, 'w', encoding = 'utf-8') as new_file:
                        new_file.write(new_text)
    with open('test_volumes_output\\test_volumes_output_table.csv', 'w', encoding = 'utf-8') as new_table_file:
        new_table_file.write(new_table)

if __name__ == '__main__':
    main()

