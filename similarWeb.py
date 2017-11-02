from selenium import webdriver
import csv
import win32api
import time
#Traffic Info miner from SimilarWeb.comCount
# Parameter : list of string, the url
# Return : list of list of statistic and url.
def trafficInfo(url):
    browser = webdriver.Firefox()
    aList=[]
    print(len(url))
    errorCount=0
    for i in range(0,len(url)):
        browser.implicitly_wait(10)
        browser.get("https://www.similarweb.com/website/{0}".format(url[i]))
        stuff2 = browser.find_elements_by_xpath("/html/body/div[1]/main/div/div/div[4]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/span[2]/span[1]")
        time.sleep(30)
        stuff2 = browser.find_elements_by_xpath("/html/body/div[1]/main/div/div/div[4]/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/span[2]/span[1]")
        aNum = "Unknown"
        try:
            print(stuff2[0].text)
            if stuff2[0].text[-1] == "M":
                aNum = str(float(stuff2[0].text[:-1])*1000000)
            elif stuff2[0].text[-1] == "K":
                aNum = str(float(stuff2[0].text[:-1])*1000)
            elif stuff2[0].text[-1] == "B":
                aNum = str(float(stuff2[0].text[:-1])*1000000000)
            else:
                aNum = stuff2[0].text[1:]
            if errorCount >= 1:
                errorCount = 0
        except:
            errorCount = errorCount + 1
            print("error: {0}, ErrorCount: {1}".format(str(i),str(errorCount)))
            if errorCount >= 10:
                win32api.MessageBox(0, 'Exit at ' + str(datetime.datetime.now()), 'Alert')
                return aList
        aList.append([aNum,url[i]])
    return aList

def TrafficReader(filename):
    aDict = {}
    with open("{0}.csv".format(filename),"r") as f:
        reader = csv.reader(f)
        for row in reader:
            aDict[row[0]] = row[2]
    return aDict
