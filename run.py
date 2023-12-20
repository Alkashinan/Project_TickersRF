
import unittest

# Importing the test cases from the test_main.py file
from test_main import TestMain

# Running the tests and capturing the output
if 1:
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
    unittest.TextTestRunner().run(suite)