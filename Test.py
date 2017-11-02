import jsonReader
import webhose
import senti
import tfidf
import LDA
import csv
import duplicateRemove
import similarWeb
import sys
maxInt=sys.maxsize
decrement = True
while decrement:
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True

def TweeterTest(tweetCsv,writename):
    data = []
    with open("{0}.csv".format(tweetCsv),"r",encoding="utf-8") as f:
        reader = csv.reader(f)
        abool = False
        for row in reader:
            if abool:
                data.append(row)
            else:
                abool = True
    for i in range(0,len(data)):
        if data[i][1][4:7] == "Jul":
            data[i][1] = "07/" + data[i][1][8:10] + "/2017"
        else:
            data[i][1] = "06/" + data[i][1][8:10] + "/2017"
        data[i] = data[i] + senti.AnalyzeTweets(data[i][0])
        print(i)
    toCsvFile(writename,data)

def RunTest(aBoolean,jsonFileName):
    if aBoolean:
        webhose.webScrape(jsonFileName)
    text = jsonReader.jsonReader(jsonFileName)
    text1 = jsonReader.jsonReaderOther(jsonFileName)
    return (text,text1)

#Exporting just the articles as csv
def writeArticles(aBoolean,jsonFileName,writename):
    aTuple = RunTest(aBoolean,jsonFileName)
    text=aTuple[0]
    text1=aTuple[1]
    aList =[]
    for line in text:
        aList.append([line])
    jsonReader.toCsvFile(writename,aList)
#Exporting Article as txt file
def writeTxtArticle(aBoolean,jsonFileName,writename):
    aTuple = RunTest(aBoolean,jsonFileName)
    text=aTuple[0]
    text1=aTuple[1]
    for i in range(0,len(text)):
        jsonReader.toTxtFile("Article{0}".format(str(i+1)),text[i])

def writeBigText(aBoolean,jsonFileName,writename):
    aTuple = RunTest(aBoolean,jsonFileName)
    text=aTuple[0]
    text1=aTuple[1]
    theString = " ".join(text)
    jsonReader.toTxtFile(writename,theString)
writeBigText(False,"theJson1","MayJune")
writeBigText(False,"theJson2","JuneJuly")
#Perform LDA
def LDATest(aBoolean,jsonFileName,writename):
    aTuple = RunTest(aBoolean,jsonFileName)
    text=aTuple[0]
    text1=aTuple[1]
    theList = LDA.LDA(text,100,10)
    FinalList = LDA.aggregate(LDA.spliter(theList))
    LDA.toCsvFile(writename,FinalList)

#Perform Tfidf
def TFIDFTest(aBoolean,jsonFileName,writename):
    aTuple = RunTest(aBoolean,jsonFileName)
    text=aTuple[0]
    text1=aTuple[1]
    The = tfidf.Tfidf(text)
    for item in The:
        print(item)
    tfidf.toCsvFile(writename,The)

#naming the article by the website
def writeTxtArticle2(aBoolean,jsonFileName):
    aTuple = RunTest(aBoolean,jsonFileName)
    text=aTuple[0]
    text1=aTuple[1]
    text = jsonReader.jsonReaderOther(jsonFileName)
    for keys in text.keys():
        for i in range(0,len(text[keys])):
            jsonReader.toTxtFile("{0}{1}".format(text[keys][i][1][:-4],i+1),text[keys][i][0])

#Getting Traffic Information
def TrafficTest(aBoolean,jsonFileName,writename):
    aTuple = RunTest(aBoolean,jsonFileName)
    text=aTuple[0]
    text1=aTuple[1]
    aList=[]
    for item in text1.keys():
        aList.append(item)
    trafficInfo = similarWeb.trafficInfo(aList)
    jsonReader.toCsvFile(writename,trafficInfo)
#TrafficTest(False,"theJson2","newWebsite")
#SentenceAnalyze
def SentenceAnalyzeByWebsite(aBoolean,jsonFileName,writename):
    aTuple = RunTest(aBoolean,jsonFileName)
    text=aTuple[0]
    text1=aTuple[1]
    for keys in text1.keys():
        aList = []
        for i in range(0,len(text1[keys])):
            aList.append(text1[keys][i][0])
        senti.SentenceAnalyze(aList,keys)
        print(keys)
#Does everything from webscraping to removing duplicates
#Need a separate websites.csv
def UltimateTest(aBoolean,jsonFileName,writename):
    aTuple = RunTest(aBoolean,jsonFileName)
    text=aTuple[0]
    text1=aTuple[1]
    The = tfidf.Tfidf(text)
    websites = similarWeb.TrafficReader("websites")
    aList = []
    bList = []
    cList = []
    numList = []
    NER = {}
    Ngram = {}
    TFIDF = {}
    noWebsite=[]
    #gets all the information from text1 dictionary into aList
    for keys in text1.keys():
        for i in range(0,len(text1[keys])):
            aList.append(text1[keys][i])
    #Counting for print
    j=0
    for item in aList:
        website = 3.69897
        #dictionary is populated with sentiment + website stuff
        try:
            website = websites[item[1]]
        except:
            print("no index")
            noWebsite.append(item[1])
        info = senti.TotalAnalysis(item[0]) + [website,item[0],item[1],item[2],item[3][:10],item[4],item[5]]
        bList.append(info)
        numList.append(float(info[14]))
        print(j)
        j=j+1
    #for normalizing the standard reading level
    maxNum = float(max(numList))
    minNum = float(min(numList))
    i=0
    #writes raw file
    toCsvFile(writename, bList)
    #attaches weight and multiplies them for all tags
    for item1 in bList:
        weight = inverseAtOne(((float(item1[14])-minNum)/(maxNum-minNum))+0.5)*(float(item1[17])-2.69897)
        vader = item1[4]*weight
        afinn = item1[5]*weight
        for line in The[i]:
            if line != None or len(line) != 0:
                try:
                    TFIDF[line[0]] = TFIDF[line[0]]+weight
                except:
                    TFIDF[line[0]] = weight
        for words in item1[15]:
            if words != None or len(line) != 0:
                try:
                    Ngram[words] = Ngram[words] + weight
                except:
                    Ngram[words] = weight
        for pair in item1[16]:
            if pair != None or len(line) != 0:
                try:
                    NER[pair[0]][2] = NER[pair[0]][2] + weight
                except:
                    NER[pair[0]] = [pair[0],pair[1],weight]
        cList.append([vader,afinn,weight])
        i=i+1
    #addes the new vader, afinn and
    for i in range(0,len(bList)):
        bList[i] = bList[i]+cList[i]+[The[i]]
    #aggregation
    NER = dictToListMulti(NER)
    Ngram = dictToListSingle(Ngram)
    TFIDF = dictToListSingle(TFIDF)
    toCsvFile("NERstat",NER)
    toCsvFile("Ngramstat",Ngram)
    toCsvFile("TFIDFstat",TFIDF)
    toCsvFile("Sentiment",bList)
    duplicateRemove.duplicateRemove("Sentiment",writename+"DR")
#NER and Ngram is dictionary of words
#bList is what needs to be written in csv

def dictToListSingle(aDict):
    aList=[]
    for keys in aDict.keys():
        aList.append([keys,aDict[keys]])
    return aList

def dictToListMulti(aDict):
    aList = []
    for keys in aDict.keys():
        bList = []
        for item in aDict[keys]:
            bList.append(item)
        aList.append([keys]+bList)
    return aList

def toCsvFile(writeName,aList):
    ofile  = open("{0}.csv".format(writeName), "w",newline="",encoding='UTF-8')
    writer = csv.writer(ofile)
    for line in aList:
        writer.writerow(line)
    ofile.close()

def inverseAtOne(aNum):
    if aNum > 1:
        dif = aNum - 1
        return 1-dif
    elif aNum < 1:
        dif = 1 - aNum
        return 1+dif
    else:
        return 1

UltimateTest(True, "DataNov","OutputNov")
#duplicateRemove.duplicateRemove("Sentiment","DuplicateRemoved5")
#TweeterTest("Tweets","heynow")
