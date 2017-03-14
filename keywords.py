import math
from textblob import TextBlob as tb
import csv
import bs4
import requests
import inspect
import locale
import smtplib
 

locale.setlocale(locale.LC_ALL,'en_US.UTF-8')


def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
	w=len(bloblist) / (1 + n_containing(word, bloblist))
	if (w<=0):
		w=1
	return math.log(w)

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def loadcsv(filename):
	lines=csv.reader(open(filename,"rb"))
	dataset=list(lines)
	for i in range(len(dataset)):
			dataset[i]=[x for x in dataset[i]]
	return dataset

def seperateByClass(dataset):
	seperated=[]
	for i in range(len(dataset)):
		vector=dataset[i]
		a=vector[0]
		vector[0]=tb(a)
		seperated.append(vector[0])
	return seperated

def csvAdd(dict_data,columns):
    try:
        with open('testit.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile,columns)
            for data in dict_data:
                writer.writerow(data)
                print data





    except  Exception as e:
        #print inspect.stack()
        print e

def test(test):
	name="filename"
	columns=["issue"]
	dict_data=[{"issue": test}]
	csvAdd(dict_data,columns)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("sukhad.anand@gmail.com", "desertstorm")
	dataset=loadcsv("testit.csv")
	bloblist = seperateByClass(dataset)
	l=len(bloblist)
	fre={}
	c=0
	for i, blob in enumerate(bloblist):
	    print("Top words in document {}".format(i + 1))
	    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
	    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
	    for word, score in sorted_words[:2]:
	        if word not in fre:
	        	fre[word]=1
	        else:
	        	fre[word]=fre[word]+1
	        if(fre[word]>len(bloblist)/2 and i==l-1 and c==0):
	        	c=1
	        	msg = test
	        	server.sendmail("sukhad.anand@gmail.com", "kohlishivam5522@gmail.com", msg)
	        	server.quit()    
test("it is amazing")

