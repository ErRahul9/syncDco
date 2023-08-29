import os
import sys
from sys import argv

from dotenv import load_dotenv

from auto.jsonReader import jsonReader
from syncDco import *
from syncDco.main import main

if __name__ == '__main__':
    load_dotenv()
    # fixpath = os.path.join(sys.path[0], "fixtures")
    # testFileName = argv[1] + "_test.json"
    # testCases = jsonReader(fixpath, testFileName).readJson()
    # allTests = testCases.get(argv[1]).keys()
    # # print(testCases.get(argv[1]))
    # if len(sys.argv) == 3:
    #     print("running test for {}".format(argv[2]))
    #     allTests = list(filter(lambda test: (test in argv[2]), allTests))
    # for test in allTests:
    #     print(test)
    #     print(argv[1])
    #     main(test, argv[1]).refreshSecurityToken()
    #     getResponse = main(test, argv[1]).ValidateResposeData(test)

    # # print(testCases.get("threshold").get("DCONetworkThreshold0"))
    main("DCOPublisherPerformanceThreshold99", "threshold").refreshSecurityToken()
    # main("DCONetworkThresholdIsZero","threshold").ValidateResposeData("DCONetworkThresholdIsZero")
    # main("DCONetworkThresholdInt", "threshold").ValidateResposeData("DCONetworkThresholdInt")
    # main("DCOPublisherPerformanceThresholdStringValueNeg_decimal", "threshold").ValidateResposeData("DCOPublisherPerformanceThresholdStringValueNeg_decimal")
    # main("DCOPublisherPerformanceThresholdStringValue", "threshold").ValidateResposeData("DCOPublisherPerformanceThresholdStringValue")


    #






    # (main("test1", "campaigns").verifyBeeswax(137231))




