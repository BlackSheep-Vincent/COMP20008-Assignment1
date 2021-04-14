## Part B Task 3
import re
import sys
import pandas as pd
import nltk
import os

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
    count = 0
    file = 'python partb2.py ' + 'cricket'+ txt # group the command name
    obtain = os.popen(file, 'r')
    article = obtain.read() # obtain the output string in partb2
    obtain.close()
    
    # test all the words with keywords whether they are the same
    for keyword in range(len(command)):
        word = command[keyword]
        if re.search(r'( '+ word +' )|(^'+ word +' )|( '+ word +'$)', article):
            count += 1
    
    # all the keywords are occurred in the text
    if count == len(command):
        have_all_file.append(txt)

# match all eligible txt file to their own documentID and output
for txtfile in range(len(have_all_file)):
    position = DF_docID[DF_docID['filename']==have_all_file[txtfile]]['documentID']
    print(position.values[0])
