# Library imports
import os
import unittest

def apiUnitTest():
    testloader = unittest.TestLoader()
    testdir = os.path.join(os.path.dirname(__file__),'apitests')
    testsuite = testloader.discover(testdir,pattern='*Testing.py')
    testrunner = unittest.TextTestRunner()
    testrunner.run(testsuite)

def apiStressTest():
	filename = os.path.join(os.path.dirname(__file__),'apitests','locustfile.py')
	os.system('locust -f ' + filename + ' --host http://localhost:5000 --users 100 --spawn-rate 2 --tags POST')

# Run every test in the testing directory
if __name__ == '__main__':
	apiUnitTest()
	apiStressTest()