#!/usr/bin/env python
import unittest
import xmlrunner
from TestMasyuBoard import *
from TestSolveMasyu import *
from TestMasyuTXT import *

suite = unittest.TestSuite()
suite.addTests( unittest.makeSuite( TestMasyuBoard ) )
suite.addTests( unittest.makeSuite( TestSolveMasyu ) )
suite.addTests( unittest.makeSuite( TestMasyuTXT ) )


if __name__=="__main__":
	testsRan = xmlrunner.XMLTestRunner().run( suite )
	exit( len( testsRan.failures ) + len( testsRan.errors ) )
