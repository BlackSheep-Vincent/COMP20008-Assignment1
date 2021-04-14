# Part B Task 2
import re
import os
import sys
from string import punctuation
from string import digits

# turn to lower case
def tolowercase(text):
    text = text.lower()
    return text

# substitution
def removecharacter(text):
    text = re.sub(r'[{}]+'.format(punctuation+digits), '', text)
    return text

# replacement        
def replacement(text):
    replace_list = ['\n','\t']
    for item in replace_list:
        text = text.replace(item,' ')    
    return text

# remove the extra white spaces in text
def removewhitespace(text):
    text = re.sub(r'\s{2,}', r' ', text)
    if text[len(text)-1] == ' ':
        text = text[:len(text)-1]
    if text[0] == ' ':
        text = text[1:]
    return text

command = sys.argv[1]

# change the present directory and get all txt name
path = "/home/jovyan/Assignment_1/cricket"
os.chdir(path)

target_file = []

# recorrect the txt file name in command line
file_name = r'\d{3,3}.txt'
command = re.findall(file_name, command)
command = command[0]

file = open(command, 'r')
target_file = file.read()
file.close()

# handing the origin text
target_file = tolowercase(target_file)
target_file = removecharacter(target_file)
target_file = replacement(target_file)
target_file = removewhitespace(target_file)

# output the precessed text
print(target_file)        