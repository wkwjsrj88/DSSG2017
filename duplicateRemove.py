from sklearn.feature_extraction.text import CountVectorizer
import csv
import pandas as pd
#Generic CSV File reader
# Parameter : filename - string as name of the filename
# Return : list of lists, each row as list
def readCSV(filename):
    aList=[]
    with open("{0}.csv".format(filename),"r",encoding='UTF-8') as f:
        reader = csv.reader(f)
        for row in reader:
            aList.append(row)
    return aList
# Duplicate Remover, threshhold is set at .9
# Parameter : filename - string as name of input filename
#           : writename - string as output name
# Return : None, writes csv file
def duplicateRemove(filename,writeName):
    originalList = readCSV(filename)
    originalList2= originalList
    i=0
    aNum=len(originalList)
    while i <= aNum:
        indexList=[i]
        print("on document: {0}".format(i))
        longest=i
        countvec = CountVectorizer()
        try:
            if len(originalList[i][18]) >= 3:
                stuff2 = pd.DataFrame(countvec.fit_transform([originalList[i][18]]).toarray(),columns=countvec.get_feature_names())
                for j in range(i+1,len(originalList)):
                    if len(originalList[j][18]) >= 3:
                        stuff3 = pd.DataFrame(countvec.fit_transform([originalList[j][18]]).toarray(),columns=countvec.get_feature_names())
                        if compareDF(stuff2,stuff3) >= 0.9:
                            indexList.append(j)
                print("length of duplicate is {0}".format(len(indexList)-1))
                if len(indexList) > 1:
                    traffic = 0
                    for num in indexList:
                        traffic = traffic + float(originalList[num][17])-2.69897
                        if originalList[longest][18] < originalList[num][18]:
                            longest = num
                    del indexList[indexList.index(longest)]
                    indexList = sorted(indexList,reverse=True)
                    print("longest is: {0}".format(longest))
                    print(indexList)
                    originalList[longest].append(traffic)
                    for nu in indexList:
                        del originalList[nu]
                else:
                    originalList[longest].append(float(originalList[i][17])-2.69897)
                    print("No duplicate found")
        except:
            print("index out of range or random error occured")
        aNum = len(originalList)
        if longest == i:
            i=i+1
    for k in range(0,len(originalList)):
        try:
            newWeight = (float(originalList[k][24])/(float(originalList[k][17])))*float(originalList[k][26])
            originalList[k].append(float(originalList[k][22])/float(originalList[k][24])*newWeight)
            originalList[k].append(float(originalList[k][23])/float(originalList[k][24])*newWeight)
        except:
            print("index doesn't exist when re weighting")
    newList = []
    for item in originalList:
        if float(item[4]) != 0 and float(item[5]) != 0:
            newList.append(item)
    toCsvFile(writeName,originalList)

#Generic CSV File writer
# Parameter : writeName - string as name of the filename
#           : aList - list of list, where the inner list is a row
# Return : None, writes csv file
def toCsvFile(writeName,aList):
    ofile  = open("{0}.csv".format(writeName), "w",newline="",encoding='UTF-8')
    writer = csv.writer(ofile)
    for line in aList:
        writer.writerow(line)
    ofile.close()

#Comparing two Datafram
# Parameter : DF1 - scikit dataframe
#           : DF2 - sciket dataframe
# Return : percentage of how much of it being same
def compareDF(DF1, DF2):
    count = 0
    for word in DF1.axes[1]:
        try:
            if DF2[word][0] == DF1[word][0]:
                count = count+1
        except:
            count = count
    return count/len(DF1.axes[1])

def aggregateTweets(filename,writename):
    originalList = readCSV(filename)
    for i in range(0,len(originalList)):
        originalList[i].append(1)
    i=0
    aNum=len(originalList)
    while i <= aNum:
        indexList=[i]
        print("on document: {0}".format(i))
        longest=i
        try:
            if len(originalList[i][3]) >= 3:
                for j in range(i+1,len(originalList)):
                    if len(originalList[j][3]) >= 3:
                        if originalList[i][3] == originalList[j][3]:
                            indexList.append(j)
                print("length of duplicate is {0}".format(len(indexList)-1))
                if len(indexList) > 1:
                    for num in indexList:
                        if originalList[longest][3] < originalList[num][3]:
                            longest = num
                    del indexList[indexList.index(longest)]
                    indexList = sorted(indexList,reverse=True)
                    print("longest is: {0}".format(longest))
                    print(indexList)
                    originalList[longest][6] = len(indexList)+1
                    for nu in indexList:
                        del originalList[nu]
                else:
                    print("No duplicate found")
        except:
            print("index out of range or random error occured")
        aNum = len(originalList)
        if longest == i:
            i=i+1
    toCsvFile(writename,originalList)
