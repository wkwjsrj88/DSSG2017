from gensim import corpora, models
import gensim
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from stop_words import get_stop_words
import string
import csv

# Parameter : textLists - list of list that contains word tokenized documents
#           : topicNum - integer, number of topics
#           : wordNum - integer, numer of word in each topic
# Return : list of strings, the string is equation
#texts is list that contains words are tokenized document
def LDA(textsList,topicNum,wordNum):
    texts=[]
    for text in textsList:
        texts.append(cleanText(text))
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=topicNum, id2word = dictionary, passes=20)
    return ldamodel.print_topics(num_topics=topicNum,num_words=wordNum)

#Text Cleaner for LDA
def cleanText(data):
    data = re.sub(r"[^a-zA-Z0-9!\"'():;?!,.-_\s]",'',data)
    data = data.replace("\n"," ") #gets rid of new line
    translator=str.maketrans(' ',' ',string.punctuation+"\""+"“"+"”")
    data = data.translate(translator)
    words = word_tokenize(data)
#gets rid of stop words, lowercase all words
    stop = get_stop_words('en')
    tokens = [i.lower() for i in words if i not in stop]
    return tokens

#Generic CSV File writer
# Parameter : writeName - string as name of the filename
#           : aList - list of list, where the inner list is a row
# Return : None, writes csv file
def toCsvFile(writeName,aList):
    ofile  = open("{0}.csv".format(writeName), "w",newline="")
    writer = csv.writer(ofile)
    for line in aList:
        writer.writerow(line)
    ofile.close()
#LDA responce spliter
# Parameter : ldaOutput - list of list
# Return : splited List
def spliter(ldaOutput):
    LastList=[]
    for i in ldaOutput:
        theList = i[1].split("+")
        aList = []
        for item in theList:
            small = item.split("*")
            smallList = [float(small[0]),small[1].strip().replace('"','')]
            aList.append(smallList)
        LastList = LastList+aList
    return LastList
#wordlist aggregator
# Parameter : wordList - list of string with weight
# Return : list of all the words 
def aggregate(wordList):
    aDict = {}
    for item in wordList:
        try:
            aDict[item[1]] = aDict[item[1]] + item[0]
        except:
            aDict[item[1]] = item[0]
    aList = []
    for word in aDict.keys():
        aList.append([word,aDict[word]])
    return aList
