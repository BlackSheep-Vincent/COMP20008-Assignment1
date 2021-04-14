## Part B Task 4
import re
import pandas as pd
import os
import sys
import nltk
from nltk.stem.porter import *

command = sys.argv[1:5]

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

# match all eligible txt file to their own documentID and output
for txtfile in range(len(have_all_file)):
    position = DF_docID[DF_docID['filename']==have_all_file[txtfile]]['documentID']
    print(position.values[0])