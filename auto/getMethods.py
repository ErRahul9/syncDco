import subprocess
import sys

import requests
import os.path
import uuid
import boto3
import json
from dotenv import load_dotenv



class getMethods():

	def __init__(self,test,testObj):
		load_dotenv()
		self.testObj = testObj
		# self.fixpath = globals().get("fixtures")
		self.camp = sys.path[0]
		self.fixpath = os.path.join(self.camp, "fixtures")
		# self.camp = globals().get("campaigns")
		# self.ROOTDIR = globals().get("ROOTDIR")
		self.ROOTDIR = sys.path[1]
		self.jsonObject = self.fixpath, "{0}_Test.json".format(self.testObj)
		self.test = test

	def readJson(self):
		returnJsonObjects = {}
		jsonPath = os.path.join(self.fixpath, "campaign_test.json")
		readFile = json.load(open(jsonPath))
		for Key, values in readFile.items():
			returnJsonObjects[Key] = values
		return returnJsonObjects

	def send_message(self, message, groupId=""):
		# message = self.jsonObject.get(self.testObj).get(self.test).get("payload")
		jsonObject = self.readJson()
		url = jsonObject.get(self.test).get(self.testObj).get("queueUrl")
		sqs_client = boto3.client("sqs", region_name="us-west-2")
		if groupId == "":
			groupId = "QA_Automation_Test"
		response = sqs_client.send_message(
			QueueUrl=url,
			MessageBody=json.dumps(message),
			MessageGroupId=groupId,
			# MessageGroupId="QA_Automation_Test",
			MessageDeduplicationId=str(uuid.uuid4()) + ":Automationtest"
		)
		return response

	def refreshSecurityToken(self):
		p = subprocess.Popen(['okta-awscli', '--profile', 'core', '--okta-profile', 'core'])
		print(p.communicate())

	def verifyBeeswax(self, id):
		s = requests.session()
		auth = os.environ['BEESWAX_AUTH']
		authHead = {"Content-Type": "text/plain", "Cookie": os.environ['BEESWAX_COOK']}
		pay = {"email": os.environ['BEESWAX_EMAIL'], "password": os.environ['BEESWAX_PASS'], "keep_logged_in": True}
		auth = s.post(auth, data=json.dumps(pay), headers=authHead)
		url = os.environ['BEESWAX_API']
		payload = json.dumps({"line_item_id": id})
		headers = {'Content-Type': 'application/json'}
		response = s.request("GET", url, headers=headers, data=payload)
		return response.text




# if __name__ == '__main__':
# 	message = getMethods("campaign","campaignCreateProspecting").readJson().get("campaign").get("campaignCreateProspecting").get("payload")
# 	getMethods("campaign","campaignCreateProspecting").refreshSecurityToken()
# 	getMethods("campaign","campaignCreateProspecting").send_message(message)


		




		