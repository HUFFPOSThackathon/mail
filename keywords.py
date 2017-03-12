import math
import textblob as tb
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
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

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
		vector[0]=tb(vector[0])
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
	server.login("kohlishivam5522@gmail.com", "businessman")

	bloblist = seperateByClass(dataset)
	fre={}
	for i, blob in enumerate(bloblist):
	    print("Top words in document {}".format(i + 1))
	    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
	    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
	    for word, score in sorted_words[:2]:
	        if word not in fre:
	        	fre[word]=1
	        else:
	        	fre[word]=fre[word]+1
	for value in fre :
		if(fre[word]>0):
			msg = test
			server.sendmail("kohlishivam5522@gmail.com", "kohlishivam5522@gmail.com", msg)
			server.quit()
test("roadblock")

