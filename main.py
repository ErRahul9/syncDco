import time
from datetime import datetime
import json
import os
import subprocess
import sys
import uuid

import boto3
import requests

from auto.databaseConn import connecters

from auto import *


class main():
    def __init__(self, test, mod):
        self.test = test
        self.mod = mod
        self.ROOTDIR = sys.path[1]
        self.campPath = sys.path[0]
        self.fixPath = os.path.join(self.campPath, "fixtures")
        file = open(os.path.join(self.fixPath, '{0}_test.json'.format(self.mod)))
        jsonCampaignSync = json.load(file)
        self.testObj = jsonCampaignSync.get(self.mod)

        # self.fixPath = os.path.join(self.campPath, "fixtures")
        # print(len(sys.argv))
        # if len(sys.argv) == 2:
        #     file = open(os.path.join(self.fixPath, '{0}_test.json'.format(self.mod)))
        #     jsonCampaignSync = json.load(file)
        #     self.testObj = jsonCampaignSync.get(self.mod)
        #     self.test = [keys for keys in self.testObj.keys()]
        # else:
        #     self.test = [sys.argv[2]]

    def refreshSecurityToken(self):
        p = subprocess.Popen(['okta-awscli', '--profile', 'core', '--okta-profile', 'core'])
        print(p.communicate())

    def updatePayload(self, tests):
        dt = datetime.now()
        pay = self.testObj.get(tests).get("payload")
        # pay["transactionId"] = str(uuid.uuid4())
        # pay["batchId"] = str(uuid.uuid4())
        # pay["timestamp"] = str(dt.isoformat()) + "Z"
        return pay

    def run(self, tests):
        message = self.updatePayload(tests)
        sqs_client = boto3.client("sqs", region_name="us-west-2")
        url = self.testObj.get(tests).get("queueUrl")
        groupId = uuid.uuid4()
        response = sqs_client.send_message(
            QueueUrl=url,
            MessageBody=json.dumps(message),
            MessageGroupId=str(groupId) + "QA_Automation_Test",
            # MessageGroupId="QA_Automation_Test",
            MessageDeduplicationId=str(uuid.uuid4()) + ":Automationtest"
        )
        return response

    def getTableData(self, tests):
        data = self.testObj.get(tests).get("databaseInformation")
        key = data.get("key")
        val = self.updatePayload(tests).get("campaignId")
        dataVal = data.get("getColmn")
        table = data.get("tableName")

        sql = "select {} from {} where {} = {}".format(dataVal, table, key, val)
        print(sql)
        time.sleep(30)
        result = connecters(sql).connectToPostgres()
        return result

    def teardown(self):
        caches = ["core-dev-rtb-dev-blocksite-rep-group.pid24g.clustercfg.usw2.cache.amazonaws.com"]
        retData = []
        for cache in caches:
            key = "methodCall[0]"
            metadata = "methodCall[1]"
            insertType = "delete"
            # cache = cache
            print("deleting data from cache {0}".format(cache))
            retVal = connecters.connectToCache(cache, 6379, metadata, key, "delete", insertType)
            retData.append("deleted :  " + cache + "   :" + str(retVal))
        return retData


    def verifyBeeswax(self, tests):
        s = requests.session()
        id = self.testObj.get(tests).get("payload").get("line_item_id")
        print(self.testObj.get(tests).get("payload").get("line_item_id"))
        print(self.testObj.get(tests).get("payload"))
        auth = os.environ['BEESWAX_AUTH']
        authHead = {"Content-Type": "text/plain", "Cookie": os.environ['BEESWAX_COOK']}
        pay = {"email": os.environ['BEESWAX_EMAIL'], "password": os.environ['BEESWAX_PASS'], "keep_logged_in": True}
        auth = s.post(auth, data=json.dumps(pay), headers=authHead)
        url = os.environ['BEESWAX_API']
        payload = json.dumps({"line_item_id": id})
        headers = {'Content-Type': 'application/json'}
        response = s.request("GET", url, headers=headers, data=payload)
        return response.text


    def ValidateResposeData(self, test):
        if 'frequency' in test:
            self.run(test)
            time.sleep(20)
            jobj = json.loads(self.verifyBeeswax(test))
            print(jobj.get("success"))
            assert jobj.get("success") == True
            freqObj = jobj.get("payload")[0].get("frequency_cap")
            return freqObj

        else:
            payload = self.testObj.get(test).get("payload")
            print(payload)
            response =  self.run(test)
            dataBaseinfo = self.getTableData(test)
            field = self.testObj.get(test).get("expectedResult").get("field")
            if response.get("ResponseMetadata").get("HTTPStatusCode") == 200:
                tupDb = dataBaseinfo[0]
                for details in tupDb:
                    values  = details
                if int(values) == int(float(self.updatePayload(test).get(field))):
                    print("Pass")
                else:
                    print("Expected Value is {} actual value displayed in {}".format(self.updatePayload(test).get(field),
                                                                                     values))
                    print("Fail")
            return tupDb

# if __name__ == '__main__':
#     main("test1","campaigns").refreshSecurityToken()
#     print(main("DCOFrequencyCapProspectingFunnelLevel1", "frequency").verifyBeeswax("DCOFrequencyCapProspectingFunnelLevel1"))
#     print(main("test2", "campaigns").run("test2"))
#     print(main("test3", "campaigns").run("test3"))
#     print(main("test4", "campaigns").run("test4"))
#       print(main("campaigns","campaigns").run("test1"))
#     print(main("dataBlockListGlobal", "blocklist").run("dataBlockList"))
#     print(main("DCOPublisherPerformanceThreshold","threshold").ValidateResposeData("DCOPublisherPerformanceThreshold"))
# campaign budgets, daily budget (bx) , open market cap messages , blocklist,
