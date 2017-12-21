import unittest
from MasyuBoard import *
from SolveMasyu import *

class TestSolveMasyu( unittest.TestCase ):
	def setUp( self ):
		""" setUp """
		pass

def suite():
	suite = unittest.TestSuite()
	suite.addTests( unittest.makeSuite( TestSolveMasyu ) )
	return suite

if __name__=="__main__":
	unittest.main()
