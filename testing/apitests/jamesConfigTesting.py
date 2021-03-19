# Library imports
import os
import sys
import unittest
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# Import the file to be tested
from api import jamesConfig

# Tests for cfg object in jamesConfig
class TestJamesConfig_cfg(unittest.TestCase):
    # Test that cfg is a dictionary
    def test_is_dict(self):
        self.assertIsInstance(jamesConfig.cfg,dict)
    # Test that the cfg property topicmax exists, and is an int
    def test_topicmax_is_int(self):
        self.assertIsInstance(jamesConfig.cfg['topicmax'],int)
    # Test that the cfg property topicwords exists, and is an int
    def test_topicwords_is_int(self):
        self.assertIsInstance(jamesConfig.cfg['topicwords'],int)
    # Test that the cfg property mintokenlen exists, and is an int
    def test_topicwords_is_int(self):
        self.assertIsInstance(jamesConfig.cfg['mintokenlen'],int)
    # Test that the cfg property exsnum exists, and is an int
    def test_topicwords_is_int(self):
        self.assertIsInstance(jamesConfig.cfg['exsnum'],int)
    # Test that the cfg property jdkversion exists, and is a str
    def test_jdkversion_is_str(self):
        self.assertIsInstance(jamesConfig.cfg['jdkversion'],str)
    # Test that the cfg property satraining exists
    def test_has_training_data(self):
        self.assertIn('satraining',jamesConfig.cfg)
    # Test that the cfg property repo->mallet exists, and is a str
    def test_has_mallet_repo(self):
        self.assertIsInstance(jamesConfig.cfg['repo']['mallet'],str)
    # Test that the cfg property repo->ant exists, and is a str
    def test_has_ant_repo(self):
        self.assertIsInstance(jamesConfig.cfg['repo']['ant'],str)
    # Test that the cfg property path exists, and is not empty
    def test_has_paths(self):
        self.assertIsNot(jamesConfig.cfg['path'],{})
    # Test that the cfg property path has a value for every required path, and that each of these is a str
    def test_has_required_paths(self):
        requiredpaths = ['api','sapath','safile','malletpath','malletfile','malletlogging','tmp','antpath','antfile','antbin']
        for requiredpath in requiredpaths:
            self.assertIsInstance(jamesConfig.cfg['path'][requiredpath],str)

# Run the tests
if __name__ == '__main__':
    unittest.main()