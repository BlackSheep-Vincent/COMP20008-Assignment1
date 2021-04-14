## Part B Task 5
import re
import os
import sys
import pandas as pd
import nltk
from nltk.stem.porter import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import math
from numpy import dot
from numpy.linalg import norm
import numpy as np

def cosine_sim(v1, v2):
    num = dot(v1,v2)/(norm(v1)*norm(v2))
    return round(num,4)

command = sys.argv[1:]

# change the present directory and get all txt name   
path = "/home/jovyan/Assignment_1/cricket"
os.chdir(path)
list = os.listdir("/home/jovyan/Assignment_1/cricket")

findtxt = re.compile(r'\w+\.txt')
txtlist = findtxt.findall(str(list))

# loading the csv file in partb1
DF_docID = pd.read_csv("partb1.csv", encoding='ISO-8859-1')

have_all_file = []

# change the diretory back to the previous one to execute partb2 program
os.chdir("/home/jovyan/Assignment_1")
stemlist = []
tflist = []

for txt in txtlist:
    porterStemmer = PorterStemmer()
    wordDict = {}
    count = 0

    file = 'python partb2.py ' + 'cricket'+ txt # group the command name
    obtain = os.popen(file, 'r')
    article = obtain.read() # obtain the output string in partb2
    obtain.close()
    
    # doing word tokenisation and store words in a list
    tokenize_list = nltk.word_tokenize(article)
    

    # stemming all words and store in a dictionary with their frequency
    for word in tokenize_list:
        stemword = porterStemmer.stem(word)
        
        if stemword in wordDict:
            wordDict[stemword] = wordDict[stemword] +1
        else :
            wordDict[stemword] = 1
            
    # test all stemmed words with keywords whether they are the same
    for keyword in range(len(command)):
        command_word = command[keyword]
        stem_command_word = porterStemmer.stem(command_word)
        if stem_command_word in wordDict:
            count += 1

    # all the keywords are occurred in the text
    if count == len(command): 
        have_all_file.append(txt)
        arti = ' '.join(tokenize_list)
        stemlist.append(arti)
        
if (stemlist):        
    vectorizer = CountVectorizer(analyzer ='word')        
    X = vectorizer.fit_transform(stemlist)        
    word = vectorizer.get_feature_names()
   
    X = X.toarray()     
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)

    doc_tfidf = tfidf.toarray()

    for keyword in range(len(command)):
        command_word = command[keyword]
        command[keyword] = porterStemmer.stem(command_word)

    query_vc = [0 for i in range(len(word))]

    for pos in range(len(word)):
        word[pos] = porterStemmer.stem(word[pos])
        if word[pos] in command:
            query_vc[pos] += 1


    q_unit = [x/(math.sqrt(count)) for x in query_vc]


    sims = [cosine_sim(q_unit, doc_tfidf[d_id]) for d_id in range(doc_tfidf.shape[0])]


    result = {}
    resultnumber = []

    print('documentID score')
    
    # match all eligible txt file to their own documentID and output
    for txtfile in range(len(have_all_file)):
        position = DF_docID[DF_docID['filename']==have_all_file[txtfile]]['documentID']
        documentID = position.values[0]
        score = sims[txtfile]
        result[score] = documentID

    sims = np.sort(sims)[::-1]

    for number in range(len(sims)):
        print('%-9s %+6s' %(result[sims[number]],str(sims[number])))


















