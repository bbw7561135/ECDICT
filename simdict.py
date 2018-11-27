# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:47:04 2018

@author: tedoreve
"""


from nltk.corpus import words
from nltk.corpus import wordnet
import difflib
from stardict import StarDict

#==============================================================================

def similar(word, n, cutoff):
    dic  = words.words()
    sim  = difflib.get_close_matches(word, dic, n = n, cutoff = cutoff)    
    # func = lambda x,y:x if y in x else x + [y]
    # sim  = reduce(func, [[], ] + sim)
    
    print('| 单词 |',' '*10, '  | 翻译 |',' '*62,'| 影响因子 |',' '*3,'| 音标 |')
    dc = StarDict('stardict.db')
    dictionary = dc.query_batch(sim)
    translations = list(filter(None,dictionary))
    
    for translation in translations:
        if translation['frq'] > 0:
            impactfactor = isnone(translation['oxford'])*1000000\
            +isnone(translation['collins'])*100000\
            +translation['frq']
            
            translength = translen(translation['translation'].replace('\n',''))

            
            print(translation['word'], ' '*(10-len(translation['word']))+'-> ', 
                  translation['translation'].replace('\n','')+
                  '-'*(77-translength)+'|', impactfactor, ' '*3+
                  translation['phonetic'])
        else:
            pass

    # if Google:
    #     translator1   = Translator()
    #     translations = translator1.translate(sim,dest='zh-cn')
    #     for translation in translations:
    #         print(translation.origin, ' '*(13-len(translation.origin))+'-> ', translation.text)
    # else:
    #     conn = db.connect('Mydict.db')
    #     cursor = conn.cursor()
    #     conn.row_factory = db.Row
    #     cursor.execute("select * from Words")
    #     rows = cursor.fetchall()
    #     translator2 = dict(rows)
    #     for word in sim:
    #         try:
    #             print(word, ' '*(13-len(word))+'-> ', translator2[word])
    #         except:
    #             continue
    print('')

    return translations

def isnone(score):
    if not score: 
        return 0
    else:
        return score
    
def translen(word):
    utf8_length = len(word.encode('utf-8'))
    length      = len(word)
    return int(((utf8_length - length)/2)*0.63) + length
#==============================================================================

def meaning(sim):
    synonyms = []
    
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
                 synonyms.append(lm.name())
    print (set(synonyms))
    
    antonyms = []
    
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            if lm.antonyms():
                antonyms.append(lm.antonyms()[0].name())
    
    print(set(antonyms))
    return '有空做个APP'
    
#==============================================================================
if __name__ == '__main__':
    word    = 'farmer'  
    n       = 100          #upper limit number of similar words
    cutoff  = 0.8         #larger value means less words
    sim     = similar(word, n, cutoff)
    app     = meaning(sim)