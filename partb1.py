## Part B Task 1
import re
import pandas as pd
import os
import sys

command = sys.argv[1]

# change the present directory and get all txt name
path = "/home/jovyan/Assignment_1/cricket"
os.chdir(path)
list = os.listdir("/home/jovyan/Assignment_1/cricket")

# make sure getting all txt file
findtxt = re.compile(r'\w+\.txt')
txtlist = findtxt.findall(str(list))

docID_data = []

# firstly find similar pattern which can have at most 3 letters at behind
pattern = r'[A-Z]{4,4}-\d{3,3}[a-zA-Z]{0,3}'

notlett_cond = r'[A-Z]{4,4}-\d{3,3}' # don't have optional letter
lett_cond = r'[A-Z]{4,4}-\d{3,3}[A-Z]' # have optional letter

# three judgment conditions
judg1 = r'([A-Z]{2,2}[a-z])' 
judg2 = r'[A-Z][a-z]{1,2}'
judg3 = r'\d[A-Z]{2,2}'

# search for each line in each txt file
for txt in txtlist:
    file = open(txt,'r')
    for line in file.readlines():
        if re.search(pattern, line):
            result = re.findall(pattern, line)
    # 1st condition        
    if re.search(judg1, str(result)):
        answer = re.findall(lett_cond, str(result))
    # 2nd condition
    elif re.search(judg2, str(result)):
        answer = re.findall(notlett_cond, str(result))
    # 3rd condition
    elif re.search(judg3, str(result)):
        answer = re.findall(lett_cond, str(result))
    # origin form
    else:
        answer = result
    
    # stored searching result in a list
    docID_data.append(answer[0])
    file.close()

# create data frame and save csv file
filename = pd.Series(txtlist)
docID = pd.Series(docID_data)
df = pd.DataFrame({'filename': filename, 'documentID': docID}).set_index('filename')

df.to_csv(command)











