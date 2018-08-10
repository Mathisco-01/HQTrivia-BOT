import os
import boto3
from datetime import datetime, time
import jmespath
import json
import urllib
from bs4 import BeautifulSoup

t1 = datetime.now()

cwd = os.getcwd()

if __name__ == "__main__":
	bucketName ='hqtriviabucket'
	photo = 'screenshot.jpg'

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
		
	return question, awnsers	

		

array = []


#upload()
#checkText()
question, awnsers = getAwnser()
print(question)
print(awnsers)


url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'
response = urllib2.urlopen(url)
webContent = response.read()

t2 = datetime.now()

print(t2 - t1)