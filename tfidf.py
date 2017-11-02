from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import csv

# Parameter : list of strings where string is a long text
# Return :  list of tfidf words and score
def Tfidf(articles):
    vectorizer = TfidfVectorizer(analyzer='word',ngram_range=(1,3),min_df=0,stop_words="english")
    vectors = vectorizer.fit_transform(articles)
    features = vectorizer.get_feature_names()
    dense = vectors.todense()
    theDict=[]
    print(len(dense))
    for i in range(0,len(dense)):
        aList=[]
        episode = dense[i].tolist()[0]
        phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]
        sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
        for phrase, score in [(features[word_id], score) for (word_id, score) in sorted_phrase_scores][:10]:
            aList.append((phrase,score))
        theDict.append(aList)
    return theDict

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
