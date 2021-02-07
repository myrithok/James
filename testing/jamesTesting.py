# Library imports
import os
import unittest

# Run every test in the testing directory
if __name__ == '__main__':
    testloader = unittest.TestLoader()
    testdir = os.path.join(os.path.dirname(__file__),'tests')
    testsuite = testloader.discover(testdir,pattern='*Testing.py')
    testrunner = unittest.TextTestRunner()
    testrunner.run(testsuite)