from nltk.tokenize import sent_tokenize
import csv
def TxtToCsv(filename,output):
    what = open(filename,"r")
    data = " ".join(what.readlines())
    print(data)
    tokens = sent_tokenize(data)
    ofile  = open(output, "w")
    writer = csv.writer(ofile)
    for line in tokens:
        writer.writerow([line])
    ofile.close()
    what.close()
TxtToCsv("Article3.txt","Article3.csv")
