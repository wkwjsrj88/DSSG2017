import csv
import re
dateList = []
# This reads finished tweet data to readable csv for R program
# The the key for the aggregation is date where the tweet happened
# Parameter - filname : list of string,
#           - writename : string,
# Return - None, saves the processed data as outputname in csv
def ProcessTweets(filename,writename):
    aDict = {}
    with open("{0}.csv".format(filename),"r",encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                aDict[row[1]].append(row)
            except:
                aDict[row[1]] = [row]
    newList=[]
    for key in aDict.keys():
        aList = []
        AFINN = 0
        Vader = 0
        Label = 0
        for item in aDict[key]:
            aList.append((item[3],item[6]))
            AFINN = AFINN + float(item[5])*float(item[6])
            Vader = Vader + float(item[4])*float(item[6])
            Label = Label + float(item[2])*float(item[6])
        aList = sorted(aList,key = lambda what: what[1],reverse=True)
        bList = []
        for item in aList:
            bList.append(item[0] + " Tweeted: " + str(item[1]))
        newList.append([key,bList,Label,Vader,AFINN])
    toCsvFile(writename,newList)
# Simple csv reader for news article data. puts the data into dictionary
# The the key for the aggregation is date and the traffic level.
# Parameter - filname : list of string,
# Return - dictionary of dictionary of list : first key is traffic, then date
def CsvReader(filename):
    aDict = {}
    aDict[3]={}
    aDict[4]={}
    aDict[5]={}
    aDict[6]={}
    aDict[7]={}
    aDict[8]={}
    aDict[9]={}
    with open("{0}.csv".format(filename),"r",encoding="utf-8") as f:
        reader = csv.reader(f)
        abool = False
        for row in reader:
            if abool:
                dateList.append(row[21])
                if float(row[17]) >= 9:
                    try:
                        aDict[9][row[21]].append(row)
                    except:
                        aDict[9][row[21]]=[row]
                elif float(row[17]) >= 8:
                    try:
                        aDict[8][row[21]].append(row)
                    except:
                        aDict[8][row[21]]=[row]
                elif float(row[17]) >= 7:
                    try:
                        aDict[7][row[21]].append(row)
                    except:
                        aDict[7][row[21]]=[row]
                elif float(row[17]) >= 6:
                    try:
                        aDict[6][row[21]].append(row)
                    except:
                        aDict[6][row[21]]=[row]
                elif float(row[17]) >= 5:
                    try:
                        aDict[5][row[21]].append(row)
                    except:
                        aDict[5][row[21]]=[row]
                elif float(row[17]) >= 4:
                    try:
                        aDict[4][row[21]].append(row)
                    except:
                        aDict[4][row[21]]=[row]
                else:
                    try:
                        aDict[3][row[21]].append(row)
                    except:
                        aDict[3][row[21]]=[row]
            else:
                abool = True
    return aDict
# This gets rid of [] and () and parses through string to get the words
# Used for NER, Bigram and tfidf words
# Parameter - aString : text string
# Return - list of string : each string is a word
def processBasic(aString):
    what = re.sub(r"[^a-zA-Z0-9!\:;?!,.-_\s]",'',aString)
    what = what.replace("[","")
    what = what.replace("]","")
    what = what.split(",")
    aList = []
    for item in what:
        aList.append(item.strip())
    return aList
# This gets rid of [] and () and parses through string to get the words
# Then,it also attaches weight to the word. Used for NER
# Parameter - aString : text string
#           - weight : weight of the string
# Return - list of list of string and weight pair : [[string, weight],...]
def processNER(aString,weight):
    mainList = processBasic(aString)
    aList = []
    bList = []
    cList = []
    aBool = True
    for i in range(0,len(mainList)):
        if aBool:
            aList.append(mainList[i])
            aBool = False
        else:
            bList.append(mainList[i])
            aBool = True
    for j in range(0,len(bList)):
        cList.append([aList[j]+" "+bList[j],weight])
    return cList

# This gets rid of [] and () and parses through string to get the words
# Then,it also attaches weight to the word. Used for Bigram
# Parameter - aString : text string
#           - weight : weight of the string
# Return - list of list of string and weight pair : [[string, weight],...]
def processBigram(aString,weight):
    mainList = processBasic(aString)
    cList = []
    for item in mainList:
        cList.append([item,weight])
    return cList

# This gets rid of [] and () and parses through string to get the words
# Then,it also attaches weight to the word. Used for tfidf
# Parameter - aString : text string
#           - weight : weight of the string
# Return - list of list of string and weight pair : [[string, weight],...]
def processTfidf(aString,weight):
    mainList = processBasic(aString)
    aList = []
    bList = []
    cList = []
    aBool = True
    for i in range(0,len(mainList)):
        if aBool:
            aList.append(mainList[i])
            aBool = False
        else:
            bList.append(float(mainList[i]))
            aBool = True
    for j in range(0,len(bList)):
        cList.append([aList[j],bList[j]*weight])
    return cList

# This aggregates by word its weight for tifdf
# Parameter - aList : list of list of
#           - weight : weight of the string
# Return - list of list of string and weight pair : [[string, weight],...]
def combineTfidf(aList):
    aDict = {}
    bList = []
    for item in aList:
        for i in range(0,len(item)):
            if item != None and len(item) > 1:
                try:
                    aDict[item[i][0]] = aDict[item[i][0]] + item[i][1]
                except:
                    aDict[item[i][0]] = item[i][1]
    for key in aDict.keys():
        bList.append([key,aDict[key]])
    bList = sorted(bList, key=lambda what: what[1],reverse=True)
    cList=[]
    for item in bList:
        cList.append(item[0])
    return cList

def combineBigram(aList):
    aDict = {}
    bList = []
    for item in aList:
        for i in range(0,len(item)):
            if item != None and len(item) > 1:
                try:
                    aDict[item[0]] = aDict[item[i][0]] + item[i][1]
                except:
                    aDict[item[i][0]] = item[i][1]
    for key in aDict.keys():
        bList.append([key,aDict[key]])
    bList = sorted(bList, key=lambda what: what[1],reverse=True)
    cList=[]
    for item in bList:
        cList.append(item[0])
    return cList

def combineNER(aList):
    aDict = {}
    bList = []
    for item in aList:
        for i in range(0,len(item)):
            if item != None and len(item) > 1:
                try:
                    aDict[item[0]] = aDict[item[i][0]] + item[i][1]
                except:
                    aDict[item[i][0]] = item[i][1]
    for key in aDict.keys():
        bList.append([key,aDict[key]])
    bList = sorted(bList, key=lambda what: what[1],reverse=True)
    cList=[]
    for item in bList:
        cList.append(item[0])
    return cList

def combineScores(aList):
    AFINN = 0
    VADER = 0
    NER = []
    Bigram = []
    TFIDF = []
    Title = []
    for item in aList:
        try:
            AFINN = AFINN + float(item[28+2])
        except:
            print("no float for AFINN")
        try:
            VADER = VADER + float(item[27+2])
        except:
            print("no float for VADER")
        try:
            Title.append(item[22])
        except:
            print("Title didn't append")
        try:
            NER.append(processNER(item[16],float(item[26+2])))
        except:
            print("no float for NER")
        try:
            Bigram.append(processBigram(item[15],float(item[26+2])))
        except:
            print("no float for Bigram")
        try:
            TFIDF.append(processTfidf(item[25+2],float(item[26+2])))
        except:
            print("no float for TFIDF")
    #print(TFIDF)
    #print(Bigram)
    #print(NER)
    return [AFINN/max(1,len(aList)),VADER/max(1,len(aList)),len(aList),combineNER(NER)[:20],combineBigram(Bigram)[:20],combineTfidf(TFIDF)[:20],list(set(Title))]

def process(aDict):
    totalList=[]
    for key in aDict.keys():
        for key2 in aDict[key].keys():
            aList = [key,key+1,key2] + combineScores(aDict[key][key2])
            totalList.append(aList)
    for date in set(dateList):
        List3=[]
        List4=[]
        List5=[]
        List6=[]
        List7=[]
        List8=[]
        List9=[]
        try:
            List3 = aDict[3][date]
        except:
            List3 = []
        try:
            List4 = aDict[4][date]
        except:
            List4 = []
        try:
            List5 = aDict[5][date]
        except:
            List5 = []
        try:
            List6 = aDict[6][date]
        except:
            List6 = []
        try:
            List7 = aDict[7][date]
        except:
            List7 = []
        try:
            List8 = aDict[8][date]
        except:
            List8 = []
        try:
            List9 = aDict[9][date]
        except:
            List9 = []
        totalList.append([3,5,date] + combineScores(List3+List4))
        totalList.append([3,6,date] + combineScores(List3+List4+List5))
        totalList.append([3,7,date] + combineScores(List3+List4+List5+List6))
        totalList.append([3,8,date] + combineScores(List3+List4+List5+List6+List7))
        totalList.append([3,9,date] + combineScores(List3+List4+List5+List6+List7+List8))
        totalList.append([3,10,date] + combineScores(List3+List4+List5+List6+List7+List8+List9))
        totalList.append([4,6,date] + combineScores(List4+List5))
        totalList.append([4,7,date] + combineScores(List6+List4+List5))
        totalList.append([4,8,date] + combineScores(List7+List4+List5+List6))
        totalList.append([4,9,date] + combineScores(List8+List4+List5+List6+List7))
        totalList.append([4,10,date] + combineScores(List9+List4+List5+List6+List7+List8))
        totalList.append([5,7,date] + combineScores(List5+List6))
        totalList.append([5,8,date] + combineScores(List6+List7+List5))
        totalList.append([5,9,date] + combineScores(List7+List8+List5+List6))
        totalList.append([5,10,date] + combineScores(List8+List9+List5+List6+List7))
        totalList.append([6,8,date] + combineScores(List6+List7))
        totalList.append([6,9,date] + combineScores(List7+List8+List6))
        totalList.append([6,10,date] + combineScores(List8+List9+List6+List7))
        totalList.append([7,9,date] + combineScores(List7+List8))
        totalList.append([7,10,date] + combineScores(List8+List9+List7))
        totalList.append([8,10,date] + combineScores(List8+List9))
    return totalList

def toCsvFile(writeName,aList):
    ofile  = open("{0}.csv".format(writeName), "w",newline="",encoding="utf-8")
    writer = csv.writer(ofile)
    for line in aList:
        writer.writerow(line)
    ofile.close()

toCsvFile("JuneJulyFinished",process(CsvReader("JuneJuly")))
#ProcessTweets("cleanedTweetswhat","alskdfj")
