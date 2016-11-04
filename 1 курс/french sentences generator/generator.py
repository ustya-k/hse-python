import random

vowels = 'euioaééoèêhœ'

def divide(file_name):#returns a list of all of the words in file
    f = open(file_name, 'r', encoding = 'utf-8')
    words = f.read()
    f.close()
    return words.split()


def word_choice(file_name):#chooses a random word from the list
    words = divide(file_name)
    the_word = random.choice(words)
    return the_word


def cut(first_word, second_word): #contraction, ex: je aime -> j'aime
    if (first_word == 'je' or first_word == 'ne' or first_word == 'la' or first_word == 'le' or first_word == 'est-ce-que') and second_word[0] in vowels:
        return first_word[:len(first_word)-1] + '\'' + second_word
    else:
        return first_word + ' ' + second_word

    
def art(gen):#randomly chooses definite/indefinite article (singular) depending on gender (defined by a name of the file which contained it)
    fem_articles = ['une', 'la']
    masc_articles = ['un', 'le']
    if gen == 'nomsfem.txt':
        return random.choice(fem_articles)
    elif gen == 'nomsmasc.txt':
        return random.choice(masc_articles)
    else:
        return ''

    
def subj():#compiles a subject: personal pronoun/an article + noun + adjective
    files = ['nomsfem.txt', 'nomsmasc.txt', 'pronomspers.txt'] #files from which it can choose a subject
    wordtype = random.choice(files)
    sbj = word_choice(wordtype)
    wordnumber = random.randint(1, 2) #chooses number of a noun
    if wordtype != 'pronomspers.txt':
        if wordnumber == 1: #singular form
            sbj = add_art(sbj, wordtype) + ' ' + adj(wordtype)
        else: #plural form
            sbj = art_pl(sbj, wordtype) + ' ' + pl(adj(wordtype), wordtype)
    return sbj


def pl(adjective, gen):#returns an adjective in plural; gen - name of the file where was a noun, it expresses gender
    if gen == 'nomsfem.txt':#feminine nouns
        return adjective + 's'
    else: #masculine nouns
        if adjective[-1] == 'x' or adjective[-1] == 's':
            return adjective
        elif adjective[len(adjective)-2:] == 'al':
            return adjective[:len(adjective)-1] + 'ux'
        elif adjective == 'beau' or adjective == 'nouveau':
            return adjective + 'x'
        else:
            return adjective + 's'

        
def art_pl(sbj, gen):#randomly chooses defenite/indefenite article (plural); returns a noun in plural form with an article; gen - name of the file where was a noun, it expresses gender
    articles = ['les', 'des']
    article = random.choice(articles)
    irregular = ['bal', 'carnival', 'festival'] #masculine exceptions 
    if gen == 'nomsfem.txt': #making a correct form if noun is feminine
        if sbj[-1] == 's' or sbj[-1] == 'x' or sbj[-1] == 'z':
            sbj = sbj
        elif sbj[len(sbj)-2:] == 'au' or sbj[len(sbj)-2:] == 'eu' or sbj[len(sbj)-3:] == 'eau':
            sbj = sbj + 'x'
        else:
            sbj = sbj + 's'
    else: #making a correct form if noun is masculine
        if sbj[-1] == 's' or sbj[-1] == 'x' or sbj[-1] == 'z':
            sbj = sbj
        elif sbj[len(sbj)-2:] == 'au' or sbj[len(sbj)-2:] == 'eu' or sbj[len(sbj)-3:] == 'eau' or sbj[len(sbj)-2:] == 'ou':
            sbj = sbj + 'x'
        elif sbj in irregular:
            sbj = sbj + 's'
        elif sbj[len(sbj)-2:] == 'al':
            sbj = sbj[:len(sbj)-1] + 'ux'
        elif sbj == 'travail':
            sbj = 'travaux'
        elif sbj == 'œil':
            sbj = 'yeux'
        else:
            sbj = sbj + 's'
    return article + ' ' + sbj


def obj(): #compiles an object: an article + noun + an adjective
    files = ['nomsfem.txt', 'nomsmasc.txt'] #files from which it can choose an object
    wordtype = random.choice(files)
    objct = word_choice(wordtype)
    wordnumber = random.randint(1, 2) #chooses number of a noun
    if wordnumber == 1: #singular
        objct = add_art(objct, wordtype) + ' ' + adj(wordtype)
    else: #plural
        objct = art_pl(objct, wordtype) + ' ' + pl(adj(wordtype), wordtype)
    return objct


def add_art(noun, gen): #adds an article; gen - name of the file where was a noun, it expresses gender
    return cut(art(gen), noun)


def acc(v):#in four présent verb forms é -> è,  y -> i (and exactly the opposite in imparfait)
    if (v[-2] == 'é'):
        v = v[:len(v)-2] + 'è' + v[-1]
    elif (v[-2] == 'è'):
        v = v[:len(v)-2] + 'é' + v[-1]
    if (v[-1] == 'y'):
        v = v[:len(v)-1] + 'i'
    elif (v[-1] == 'i'):
        v = v[:len(v)-1] + 'y'
    return v


def verb(sbj): #chooses a transitive verb and its form depending on the subject (sbj)
    files = ['verbsItransit.txt', 'verbsIItransit.txt'] #files from which it can choose a verb
    wordtype = random.choice(files)
    v = word_choice(wordtype)
    if wordtype == files[0]: #1st group verbs
        return verb_st(v, sbj)
    elif wordtype == files[1]: #2nd group verbs
        return verb_nd(v, sbj)

    
def verb_intr(sbj): #chooses an intransitive verb and its form depending on the subject (sbj)
    files = ['verbsIintransr.txt', 'verbsIIintrans.txt'] #files from which it can choose a verb
    wordtype = random.choice(files)
    v = word_choice(wordtype)
    if wordtype == files[0]: #1st group verbs
        return verb_st(v, sbj)
    elif wordtype == files[1]: #2nd group verbs
        return verb_nd(v, sbj)

    
def verb_st(v, sbj): #1st group verb in présent
    if sbj == 'je':
        return acc(v) + 'e'
    elif sbj == 'tu':
        return acc(v) + 'es'
    elif sbj == 'nous':
        return v + 'ons'
    elif sbj == 'vous':
        return v + 'ez'
    elif sbj == 'ils' or sbj == 'elles' or sbj[:4] == 'les ' or sbj[:4] == 'des ':
        return acc(v) + 'ent'
    else:
        return acc(v) + 'e'

    
def verb_nd(v, sbj):#2nd group verb in présent
    if sbj == 'je' or sbj == 'tu':
        return v + 'is'
    elif sbj == 'nous':
        return v + 'issons'
    elif sbj == 'vous':
        return v + 'issez'
    elif sbj == 'ils' or sbj == 'elles' or sbj[:4] == 'les ' or sbj[:4] == 'des ':
        return v + 'issent'
    else:
        return v + 'it'

    
def adj(gen): #returns a random adjective in agreement in gender with a noun; gen - name of the file where was a noun, it expresses gender
    files = 'adj.txt'
    adjective = word_choice(files)
    if gen == 'nomsfem.txt': #makes a feminine adjective
        if adjective[len(adjective)-2:] == 'el' or adjective[len(adjective)-2:] == 'et' or adjective[len(adjective)-2:] == 'on' or adjective[len(adjective)-3:] == 'en':
            return adjective + adjective[-1] + 'e'
        elif adjective[-1] == 'f':
            return adjective[:len(adjective)-1] + 've'
        elif adjective[len(adjective)-3:] == 'eux':
            return adjective[:len(adjective)-1] + 'se'
        elif adjective[-1] == 'e' or adjective[-1] == 'a':
            return adjective
        elif adjective[len(adjective)-2:] == 'er':
            return adjective[:len(adjective)-2] + 'ère'
        elif adjective == 'gros':
            return adjective + 'se'
        elif adjective == 'nouveau' or adjective == 'beau':
            return adjective[:len(adjective)-2] + 'lle'
        elif adjective == 'doux':
            return 'douce'
        elif adjective == 'blanc':
            return adjective + 'he'
        elif adjective == 'frais':
            return 'fraîche'
        elif adjective == 'long':
            return adjective + 'ue'
        elif adjective == 'vieux':
            return 'vielle'
        elif adjective == 'faux' or adjective == 'roux':
            return adjective[:len(adjective)-1] + 'sse'
        else:
            return adjective + 'e'
    elif gen == 'nomsmasc.txt':
        return adjective

    
def imparfait(subject, v): #verb in imparfait
    if v[len(v)-2:] == 'is':
        return acc(v[:len(v)-2]) + 'issais'
    elif v[len(v)-2:] == 'es':
        return acc(v[:len(v)-2]) + 'ais'
    elif v[len(v)-2:] == 'it':
        return acc(v[:len(v)-2]) + 'issait'
    elif v[len(v)-3:] == 'ons':
        return acc(v[:len(v)-3]) + 'ions'
    elif v[len(v)-2:] == 'ez':
        return acc(v[:len(v)-2]) + 'iez'
    elif v[len(v)-3:] == 'ent':
        return acc(v[:len(v)-3]) + 'aient'
    elif v[-1] == 'e':
        if subject == 'je':
            return acc(v[:len(v)-1]) + 'ais'
        else:
            return acc(v[:len(v)-1]) + 'ait'

        
def conditionel(): #returns a conditional sentence
    subject = subj() #subject of the first part of the sentence
    subject2 = subj() #subject of the second part of the sentence
    v = verb(subject) #transitive verb of the first part of the sentence
    v2 = verb(subject2) #transitive verb of the second part of the sentence
    v_intr = verb_intr(subject) #intransitive verb of the first part of the sentence
    v_intr2 = verb_intr(subject2) #intransitive verb of the second part of the sentence
    sentencetype = random.randint(1, 5)
    if sentencetype == 1:#présent trans-présent trans
        return 'Si ' + cut(subject, v) + ' ' + obj() + ',  ' + cut(subject2, v2) + ' ' + obj() + '.'
    elif sentencetype == 2:#présent intrans-présent trans
        return 'Si ' + cut(subject, v_intr) + ',  ' + cut(subject2, v2) + ' ' + obj() + '.'
    elif sentencetype == 3:#présent trans-présent intrans
        return 'Si ' + cut(subject, v) + ' ' + obj() + ',  ' + cut(subject2, v_intr2) + '.'
    elif sentencetype == 4:#imparfait trans-imparfait trans
        return 'Si ' + cut(subject, imparfait(subject, v)) + ' ' + obj() + ',  ' + cut(subject2, imparfait(subject2, v2)) + ' ' + obj() + '.'
    elif sentencetype == 5:#imparfait intrans-imparfait trans
        return 'Si ' + cut(subject, imparfait(subject, v_intr)) + ',  ' + cut(subject2, imparfait(subject2, v2)) + ' ' + obj() + '.'


def positif(): #returns a positive sentence
    subject = subj() 
    v = verb(subject) #transitive verb
    v_intr = verb_intr(subject) #intransitive verb
    sentencetype = random.randint(1, 4)
    if sentencetype == 1:#présent trans
        return cut(subject, v).capitalize() + ' ' + obj() + '.'
    elif sentencetype == 2:#présent intrans
        return cut(subject, v_intr).capitalize() + '.'
    elif sentencetype == 3:#imparfait trans
        return cut(subject, imparfait(subject, v)).capitalize() + ' ' + obj() + '.'
    elif sentencetyperand == 4:#imparfait intrans
        return cut(subject, imparfait(subject, v_intr)).capitalize() + '.'

    
def negatif(): #returns a negative sentence
    subject = subj()
    v = verb(subject) #transitive verb
    v_intr = verb_intr(subject) #intransitive verb
    sentencetype = random.randint(1, 4)
    if sentencetype == 1:#présent trans
        return subject.capitalize() + ' ' + cut('ne', v) + ' pas ' + obj() + '.'
    elif sentencetype == 2:#présent intrans
        return subject.capitalize() + ' ' + cut('ne', v_intr) + ' pas.'
    elif sentencetype == 3:#imparfait trans
        return subject.capitalize() + ' ' + cut('ne', imparfait(subject, v)) + ' pas ' + obj() + '.'
    elif sentencetype == 4:#imparfait intrans
        return subject.capitalize() + ' ' + cut('ne', imparfait(subject, v_intr)) + ' pas.'

    
def interrogatif(): #returns an interrogative sentence
    subject = subj()
    v = verb(subject) #transitive verb
    v_intr = verb_intr(subject) #intransitive verb
    verbtype = random.randint(1, 2) #chooses trans/intrans verb
    questiontype = random.randint(1, 2) #chooses question type - with 'est-ce-que' or inversion
    if verbtype == 1:#présent trans
        if subject == 'je':
            quest = 'Est-ce-que ' + cut(subject, v)
        elif subject == 'tu' or subject == 'nous' or subject == 'vous' or subject == 'ils' or subject == 'elles':
            if questiontype == 1:
                quest = v.capitalize() + '-' + subject
            else:
                quest = cut('est-ce-que', subject).capitalize() + ' ' + v
        elif subject == 'elle' or subject == 'il' or subject == 'on':
            if questiontype == 1:
                if v[-1] in vowels:
                    quest = v.capitalize() + '-t-' + subject
                else:
                    quest = v.capitalize() + '-' + subject
            else:
                quest = cut('est-ce-que', subject).capitalize() + ' ' + v
        elif subject[:4] == 'les ' or subject[:4] == 'des ':#plural nouns
            if questiontype == 1:
                quest = subject.capitalize() + ' ' + v + '-ils'
            else:
                quest = 'Est-ce-que ' + cut(subject, v)
        else:
            if questiontype == 1:
                if subject[0:3] == 'une' or subject[0:2] == 'la':#feminine nouns
                    if v[-1] in vowels:
                        quest = subject.capitalize() + ' ' + v + '-t-elle'
                    else:
                        quest = subject.capitalize() + ' ' + v + '-elle'
                else:#masculine nouns
                    if v[-1] in vowels:
                        quest = subject.capitalize() + ' ' + v + '-t-il'
                    else:
                        quest = subject.capitalize() + ' ' + v + '-il'
            else:
                quest = cut('est-ce-que', subject).capitalize() + ' ' + v
        return quest + ' ' + obj() + '?'
    else:#présent intrans
        if subject == 'je':
            quest = 'Est-ce-que ' + cut(subject, v_intr)
        elif subject == 'tu' or subject == 'nous' or subject == 'vous' or subject == 'ils' or subject == 'elles':
            if questiontype == 1:
                quest = v_intr.capitalize() + '-' + subject
            else:
                quest = cut('est-ce-que', subject).capitalize() + ' ' + v_intr
        elif subject == 'elle' or subject == 'il':
            if questiontype == 1:
                if v_intr[-1] in vowels:
                    quest = v_intr.capitalize() + '-t-' + subject
                else:
                    quest = v_intr.capitalize() + '-' + subject
            else:
                quest = cut('est-ce-que', subject).capitalize() + ' ' + v_intr
        elif subject[:4] == 'les ' or subject[:4] == 'des ':
            if questiontype == 1:
                quest = subject.capitalize() + ' ' + v + '-ils'
            else:
                quest = 'Est-ce-que ' + cut(subject, v)
        else:
            if questiontype == 1:
                if subject[0:3] == 'une' or subject[0:2] == 'la':
                    if v_intr[-1] in vowels:
                        quest = subject.capitalize() + ' ' + v_intr + '-t-elle'
                    else:
                        quest = subject.capitalize() + ' ' + v_intr + '-elle'
                else:
                    if v_intr[-1] in vowels:
                        quest = subject.capitalize() + ' ' + v_intr + '-t-il'
                    else:
                        quest = subject.capitalize() + ' ' + v_intr + '-il'
            else:
                quest = cut('est-ce-que', subject).capitalize() + ' ' + v_intr
        return quest + '?'

    
def imperatif(): #returns an imperative sentence
    sbj = ['tu', 'nous', 'vous'] #an imperative form exists only for 2sg,  1pl and 2pl
    subject = random.choice(sbj)
    verbtype = random.randint(1, 2)
    if verbtype  ==  1:
        return verb(subject).capitalize() + ' ' + obj() + '!'
    else:
        return verb_intr(subject).capitalize() + '!'

    
def main():
    ch = [] #list of 0 and 1 for every type of sentence; 0 if it was generated, 1 if it wasn't
    for i in range(5):
        ch.append(0)
    while 0 in ch:
        sentencetype  = random.randint(0, 4)
        if ch[sentencetype] == 0:
            if sentencetype == 0:
                print(positif())
                ch[0] = 1
            elif sentencetype == 1:
                print(negatif())
                ch[1] = 1
            elif sentencetype == 2:
                print(interrogatif())
                ch[2] = 1
            elif sentencetype == 3:
                print(conditionel())
                ch[3] = 1
            elif sentencetype == 4:
                print(imperatif())
                ch[4] = 1

                
if __name__ == '__main__':
    main()
