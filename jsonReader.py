# coding: utf-8
import time
from selenium import webdriver
import pandas as pd
import csv
import win32api
import re

#Normal reader, only extracts text data from the webhose json file
# Parameter : string, filename
# Return : List of strings, where strings are text
def jsonReader(readName):
#all the info in the json file
    data = pd.read_json("{0}.json".format(readName))
#just the section from json that includes information from the article
    posts = pd.read_json((data['posts']).to_json(), orient = 'index')
#a list of the article texts
    text = posts['text']
    aList =[]
    for line in text:
        aList.append(re.sub(r"[^a-zA-Z0-9!\"'():;?!,.-_\s]",'',line))
    print(len(aList))
    return aList

#Reader that returns dictionary which contains site, text and section
# Parameter : readName - string of the json filename
# Return : Dictionary where the key is website url
def jsonReaderOther(readName):
    data = pd.read_json("{0}.json".format(readName))
    theDict={}
    for piece in data['posts']:
        site = piece['thread']['site']
        section = piece['thread']['section_title']
        text = piece['text']
        title = piece['thread']['title_full']
        date = piece['published']
        author = piece['author']
        try:
            theDict[site].append([text,site,section,date,title,author])
        except:
            theDict[site] = []
            theDict[site].append([text,site,section,date,title,author])
    return theDict

#Generic CSV File writer
# Parameter : writeName - string as name of the filename
#           : aList - list of list, where the inner list is a row
# Return : None, writes csv file
def toCsvFile(writeName,aList):
    ofile  = open("{0}.csv".format(writeName), "w",newline="",encoding="utf-8")
    writer = csv.writer(ofile)
    for line in aList:
        writer.writerow(line)
    ofile.close()

#Generic txt File writer
# Parameter : writeName - string as name of the filename
#           : aList - list of list, where the inner list is a row
# Return : None, writes csv file
def toTxtFile(filename,text):
    with open("{0}.txt".format(filename),"w", encoding='UTF-8') as f:
        f.write(text)
        f.close()
