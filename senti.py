#-*-coding:utf-8 -*-
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import FreqDist
from nltk import BigramCollocationFinder
from nltk import TrigramCollocationFinder
import nltk
import string
from stop_words import get_stop_words
from textstat.textstat import *
import nltk.tag.stanford as st
import re
import csv
import tfidf
from nltk.stem import WordNetLemmatizer

# These key words are the words that are given higher weights within the articles that are given
# List can be altered to give different output
Keywords=["SNAP","food","food stamp","EBT","TANF","hunger","Trump","fraud",
    "Fraud","welfare","Welfare","Supplemental Nutrition Assistance Program"]

#Loads AFINN
textdata = open("AFINN-111.txt")
afinn={}
for line in textdata:
    inst=line.split("\t")
    afinn[inst[0]]=int(inst[1])

# This function analyze tweets using the Vader and AFINN tool
# Parameter - text: String
# Returns - cleaned text input, vader score and afinn score in a list
#   cleaned text is String, vader score and afinn scores are float
def AnalyzeTweets(text):
    lemmatizer = WordNetLemmatizer()
    stops = get_stop_words('en')
    s = re.sub(r'@([^\s]*)',"",text)
    s = re.sub(r"https:([^\s]*)","",s)
    tokens = re.sub(r"<([^\s]*)>","",s)
    tokens = word_tokenize(tokens)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = [token for token in tokens if not token in stops]
    newText = ' '.join(word for word in tokens)
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(newText)
    afinnScore = calculateSentiment(tokens)
    return [newText, ss["compound"],afinnScore]

# Parameter - text: list of string, which each string represents a sentence
# Return - list of floats, which are statistics of the text
#   The statistics are Number of Sentences, Avg.Syllable per Sentence,
#   Avg.words per sentence, Avg.comma per sentence normalized vader, and AFINN scores
def AnalyzeSentiment(text):
    translator=str.maketrans(' ',' ',string.punctuation+"\"")
    sid = SentimentIntensityAnalyzer()
    aList=[]
    for sent in text:
        comma=0
        for i in range(0,len(sent)):
            if sent[i] == ",":
                comma = comma + 1
        ss = sid.polarity_scores(sent)
        data = sent.translate(translator)
        tokens = word_tokenize(data)
        afinnScore = calculateSentiment(tokens)
        syl = textstat.syllable_count(sent)
        wordc = textstat.lexicon_count(sent,False)

# prints all the score of the sentences for debugging purpose
#        for k in sorted(ss):
#            print("{0}: {1}, ".format(k,ss[k]),end="")
#        print()
        aList.append([sent,ss,1,afinnScore,syl,wordc,comma])

# weights all the sentences with keywords more
    for i in range(0,len(aList)):
        for word in Keywords:
            if word in aList[i][0]:
                aList[i][2]=aList[i][2]+1.5
                try:
                    aList[i+1][2] = aList[i+1][2]+1
                    aList[i-1][2] = aList[i-1][2]+1
                except:
                    what=123

# calculate sum of the compound
    Vscore = 0
    Fscore = 0
    sylSum = 0
    Wordsum = 0
    comCount = 0
    count1 = 0
    count = 0
    for thing in aList:
        if thing[1]["compound"] != 0:
            count=count+1
        if thing[5] >= 10 and thing[6] > 0:
            count1 = count1 + 1
            comCount = comCount + thing[6]
        Vscore = Vscore + thing[2]*thing[1]["compound"]
        Fscore = Fscore + thing[2]*thing[3]
        sylSum = sylSum + thing[4]
        Wordsum = Wordsum + thing[5]
#Debugging purpose
    #print("Average Vader Score: " + str(Vscore/max(1,count))) #All sentence
    #print("Average AFINN Score: " + str(Fscore/max(1,len(aList)))) # only the one that includes
    #print("Average Syllable per Sentence " + str(sylSum/max(1,len(aList))))
    #print("Average Word per Sentence " + str(Wordsum/max(1,len(aList))))
    #print("Average Comma per Sentence " + str(comCount/max(1,count1)))
    #print("Total Vader Score: " + str(Vscore))
    #print("Total AFINN Score: " + str(Fscore))
    return [len(text),sylSum/max(1,len(aList)),Wordsum/max(1,len(aList)),
        comCount/max(1,count1),Vscore/max(1,len(text)),Fscore/max(1,len(text))]

#AFINN Sentiment Tool
# Parameter  - ListOfVocab : list of strings, where each string is a word
# Return - integer, representing the score
def calculateSentiment(ListOfVocab):
    score=0
    for word in ListOfVocab:
        try:
            score = score + afinn[word]
        except:
            what = None
    return score

#Needs to change for stanford-ner library
#NER tool from Standford
# Parameter - text : list of strings, where each string is a word
# Return - list of tuples, (word, type)
def nameEntity(text):
    thing = st.StanfordNERTagger("C:\stanford-ner-2016-10-31\classifiers\english.all.3class.distsim.crf.ser.gz",
        "C:\stanford-ner-2016-10-31\stanford-ner.jar")
    theList = thing.tag(text)
    aList = []
    previous = 0
    aString = ""
    for i in range(0,len(theList)):
        if theList[previous][1] == theList[i][1]:
            aString = aString + " " +theList[i][0]
        else:
            aList.append([aString.strip(), theList[previous][1]])
            aString = theList[i][0]
            previous = i
    bList=[]
    for label in aList:
        if label[1] != "O":
            bList.append(label)
    return bList

#helper function to read
# Parameter - filename : string that is filename in directory
# Return - string
def ReadArticle(filename):
    with open(filename,"r") as what:
        return " ".join(what.readlines())

#helper function to clean data
# Parameter - data : string, large text usually
# Return - string, cleaned
def cleanData(data):
    #parses through string to get rid of data
    data = re.sub(r'^https?:\/\/.*[\r\n]*', '', data, flags=re.MULTILINE)
    #data = re.sub(r'[^@]+@[^@]+\.[^@]+','',data)
    data = re.sub(r'\.([a-zA-Z])', r'. \1', data) #adds space after period
    data = re.sub(r"[^a-zA-Z0-9!\"'():;?!,.-_\s]",'',data)
    data = re.sub("Getty Images","",data)
    data = re.sub("Copyright","",data)
    data = re.sub("All rights reserved.","",data)
    data = re.sub("Read More","",data)
    data = re.sub("Read more","",data)
    data = re.sub("About Us","",data)
    data = re.sub("About us","",data)
    data = data.replace("\n"," ") #gets rid of new line
    data = data.replace(" ? ", " - ") #encoding errors
    data = data.replace('\"','') # quotations
    data = data.replace("“","")
    data = data.replace("”","")
    return data

# Combines all the helper function to perform all Analysis on single text
# Parameter - data : string, large text
# Return - list of statistics and list
def TotalAnalysis(data):
    data = cleanData(data)
    raw = data
    sents = sent_tokenize(data)
#gets rid of punctuation
    translator=str.maketrans(' ',' ',string.punctuation+"\""+"“"+"”")
    data = data.translate(translator)
#tokenizes data to words
    words = word_tokenize(data)
#gets rid of stop words, lowercase all words
    stop = get_stop_words('en')
    tokens = [i.lower() for i in words if i not in stop]
#makes it into text object
    text = nltk.Text(tokens)

#bigram and trigram features
#Dubugging purpose
#    bigram=nltk.collocations.BigramAssocMeasures()
#    trigram=nltk.collocations.TrigramAssocMeasures()
#    finder = BigramCollocationFinder.from_words(text)
#    finder.apply_freq_filter(2)
#    print(finder.nbest(bigram.pmi,100))
#collocation with bigram
    ngram = []
#lemmatize all the words
    wnl=nltk.WordNetLemmatizer()
    stuff = [wnl.lemmatize(t) for t in tokens]
    Readability =[]
    NER = 0
    try:
        ngram = text.collocations()
    except:
        print("Ngram Failed")
    try:
        Readability.append(textstat.flesch_reading_ease(raw))
    except:
        print("Flesch Reading Ease Failed")
        Readability.append("None")
    try:
        Readability.append(textstat.flesch_kincaid_grade(raw))
    except:
        print("Flesch-Kincaid Grade Level Failed")
        Readability.append("None")
    try:
        Readability.append(textstat.gunning_fog(raw))
    except:
        print("Fog Scale Failed")
        Readability.append("None")
    try:
        Readability.append(textstat.smog_index(raw))
    except:
        print("SMOG Index Failed")
        Readability.append("None")
    try:
        Readability.append(textstat.automated_readability_index(raw))
    except:
        print("ARI Failed")
        Readability.append("None")
    try:
        Readability.append(textstat.coleman_liau_index(raw))
    except:
        print("Coleman Liau Failed")
        Readability.append("None")
    try:
        Readability.append(textstat.linsear_write_formula(raw))
    except:
        print("Linsear Write Failed")
        Readability.append("None")
    try:
        Readability.append(textstat.dale_chall_readability_score(raw))
    except:
        print("Dale Chall Readability Failed")
        Readability.append("None")
    try:
        Readability.append(textstat.text_standard(raw))
    except:
        print("Text Standard Failed")
        Readability.append(8)
    try:
        NER=nameEntity(words)
    except:
        print("NER Failed")

    TextStat = AnalyzeSentiment(sents)
    return TextStat+Readability+[ngram,NER]

#If there exist txt files with publisherName+number in the same directory,
#it reads the txt files and does the sentiment analysis
# Parameter - publisherName : string, the base name of the file
# Return - None, saves the aggregated data as publisherName in csv
def writeToCsv(publisherName):
    textList =[]
    toCSVList=[["Number of Sentences","Average Syllable per Sentence","Average Word per Sentence","Average Comma per Sentence",
                "Total Vader Score", "Total AFINN Score", "Flesch Reading Ease","Flesch-Kincaid Grade Level",
                "Fog Scale", "SMOG Index", "ARI", "Coleman Liau","Linsear Write","Dale Chall","Ngram","NER"]]
    for i in range(1,100):
        try:
            textList.append(ReadArticle("{1}{0}.txt".format(str(i),publisherName)))
        except:
            print("Text out of range")
    for article in textList:
        toCSVList.append(TotalAnalysis(article)+tfidf.Tfidf(textList))
    ofile  = open("{0}.csv".format(publisherName), "w",newline="")
    writer = csv.writer(ofile)
    for line in toCSVList:
        writer.writerow(line)
    ofile.close()

# Similar concept as writeToCsv, except takes in raw textstat
# Parameter - textList : list of string,
#            outputname : string,
# Return : None, saves the aggregated data as outputname in csv
def textToCsv(textList,outputname):
    toCSVList=[["Number of Sentences","Average Syllable per Sentence","Average Word per Sentence","Average Comma per Sentence",
                "Total Vader Score", "Total AFINN Score","Vader Order","AFINN order", "Flesch Reading Ease","Flesch-Kincaid Grade Level",
                "Fog Scale", "SMOG Index", "ARI", "Coleman Liau","Linsear Write","Dale Chall","Ngram","NER"]]
    for i in range(0,len(textList)):
        toCSVList.append(TotalAnalysis(textList[i])+tfidf.Tfidf(textList))
    ofile  = open("{0}.csv".format(outputname), "w",newline="")
    writer = csv.writer(ofile)
    for line in toCSVList:
        writer.writerow(line)
    ofile.close()

# This is for outputing the sentiment analysis on each sentence. Mainly for
# checking how sentiment analyzer works
# Parameter - textList : list of string,
#           - outputname : string,
# Return : None, saves the aggregated data as outputname in csv
def SentenceAnalyze(textList,outputname):
    sid = SentimentIntensityAnalyzer()
    translator=str.maketrans(' ',' ',string.punctuation+"\"")
    TotalList = [["Vader","AFINN","Syllable","Sentence","NormalVader",
                    "NormalAFINN","Normal Syllable"]]
    for i in range(0,len(textList)):
        cleanedChunk = cleanData(textList[i])
        cleanedSent = sent_tokenize(cleanedChunk)
        TotalList.append(["ArticleNumer",i+1])
        if len(cleanedSent) >= 9:
            vader=[]
            afinn=[]
            syllable=[]
            aList = []
            for sent in cleanedSent:
                comma=0
                for j in range(0,len(sent)):
                    if sent[j] == ",":
                        comma = comma + 1
                ss = sid.polarity_scores(sent)
                vader.append(ss["compound"])
                data = sent.translate(translator)
                tokens = word_tokenize(data)
                afinnScore = calculateSentiment(tokens)
                afinn.append(afinnScore)
                syl = textstat.syllable_count(sent)
                syllable.append(syl)
                aList.append([ss["compound"],afinnScore,syl,sent])
            vader = normalize(vader)
            afinn = normalize(afinn)
            syllable = normalize(syllable)
            for j in range(0,len(cleanedSent)):
                aList[j] = aList[j] + [vader[j],afinn[j],syllable[j]]
            for item in aList:
                TotalList.append(item)
        else:
            TotalList.append(["ArticleNotStored: SentenceLength < 9"])
    ofile  = open("{0}.csv".format(outputname), "w",newline="",encoding='UTF-8')
    writer = csv.writer(ofile)
    for line in TotalList:
        writer.writerow(line)
    ofile.close()

# Normalizes list of floats from 0 to 1
# Parameter - aList : list of floats or int,
# Return - list : normalized list of floats
def normalize(aList):
    maxItem = max(aList)
    minItem = min(aList)
    for i in range(0,len(aList)):
        aList[i] = (aList[i]-minItem)/max(1,(maxItem-minItem))
    return aList
