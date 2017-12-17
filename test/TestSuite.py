#!/usr/bin/env python
import unittest
import xmlrunner
from TestMasyuBoard import *

suite = unittest.TestSuite()
suite.addTests( unittest.makeSuite( TestMasyuBoard ) )

if __name__=="__main__":
	testsRan = xmlrunner.XMLTestRunner().run( suite )
	exit( len( testsRan.failures ) + len( testsRan.errors ) )
