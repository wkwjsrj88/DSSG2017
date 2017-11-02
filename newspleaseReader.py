import os
import pandas as pd
import datetime
filenameList=[]
for filename in os.listdir(os.getcwd()+"\\newsplease"):
    if filename[-4:] == "json":
        filenameList.append(filename)

def jsonReaderOther(readName):
    data = pd.read_json("{0}.json".format(readName))
    theList=[]
    date = data["publish_date"]
    return [data["text"],data["sourceDomain"],datetime.date(date[:4],date[5:7],date[8:10])]
