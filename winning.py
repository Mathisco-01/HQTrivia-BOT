import os
import boto3
from datetime import datetime, time
import jmespath
import json
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup




if __name__ == "__main__":
	
	cwd = os.getcwd()
	bucketName ='hqtriviabucket'
	photo = 'screenshot.png'
	response = ""
	question = ""
	awnsers = []
	resultStatsList = []


	rkClient=boto3.client('rekognition', region_name='eu-west-1')
	s3Client=boto3.resource('s3',  region_name='eu-west-3')






def upload():
	bucket=s3Client.Bucket(bucketName)
	with open(photo, 'rb') as data:
	    bucket.upload_fileobj(data, photo)

def checkText():
	response=rkClient.detect_text(
		Image={'S3Object':{'Bucket':bucketName,'Name':photo}})




def getAwnser():

	typeCount = 0
	awnsers = []
	types = jmespath.search('TextDetections[:-1].Type', json.loads(response))
	for i in range(len(types)):
		if(types[i] == "LINE"):
			typeCount += 1
		else:
			pass
	
	lineList = jmespath.search('TextDetections[:{}].DetectedText'.format(typeCount), json.loads(response))
	question = ' '.join(lineList[:-3])
	for i in range(3):
			awnsers.append(lineList[(-i-1)]) 
		
		

		
def googleIt(q, a):
	print(q)#question string
	print(a)#awnsers list
	


	for i in range(3):
		r = ""
		#url = "http://www.google.com/#hl=en&q={}+{}".format(q.replace(" ","+"), a[i].replace(" ", "+"))
		url = "http://www.google.com/search?q={}+{}".format(q.replace(" ","+"), a[i].replace(" ", "+"))

		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		soup = BeautifulSoup(webpage)
		print(url) 
		results = str(soup.find_all("div", id="resultStats"))
		print(results)

		for i in range(len(results)):
			if(results[i].isdigit() == True): 
				r += results[i]
			else:
				pass
		resultStatsList.append(r)
		
	return resultStatsList





array = []


upload()
print("Upload Complete")
checkText()
print("Text Checked")
print(question, awnsers)
getAwnser()
print("Awnsers recieved")
resultStatList = googleIt(question, awnsers)


print(resultStatList)
print(max(resultStatList))
