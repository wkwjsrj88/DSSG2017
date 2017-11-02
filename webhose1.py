#Document written for python 3.5

import webhoseio
import time
import json

# Scrapes and saves the articles on SNAP on local directory
# Parameter : filename - string,
# Return : None, but saves the file
def webScrape(filename):
    webhoseio.config(token="176abb26-c7df-40b8-9d31-e3f62f955996") #Jihwan Oh's Token
    Originaloutput = webhoseio.query("filterWebContent", {"q":"""thread.title:\\"food stamp\\" site_type:news language:english EBT OR SNAP is_first:true""","ts":time.time()-2591900})
    output = Originaloutput
    aList = []
    previousLen=0
    totalResults = output["totalResults"]
    print(output["requestsLeft"])
    print(output["totalResults"])
    while len(Originaloutput["posts"]) != totalResults:
        previousLen=len(Originaloutput["posts"])
        output = webhoseio.get_next()
        if len(output["posts"])!=0:
            Originaloutput["posts"] = Originaloutput["posts"] + output["posts"]
        print(len(Originaloutput["posts"]))
    print(len(Originaloutput["posts"]))
    with open("{0}.json".format(filename),'w') as f:
        json.dump(Originaloutput,f)


#webScrape("theJson2")
