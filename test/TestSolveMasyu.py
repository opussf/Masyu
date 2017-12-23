import unittest
from MasyuBoard import *
from SolveMasyu import *

class TestSolveMasyu( unittest.TestCase ):
	def setUp( self ):
		""" setUp """
		board = MasyuBoard.MasyuBoard()
		board.loadFromFile( "puzzles/puzzle_0.txt" )
		self.Masyu = SolveMasyu( board )
	def test_Masyu_hasBoard( self ):
		self.assertTrue( self.Masyu.board )


def suite():
	suite = unittest.TestSuite()
	suite.addTests( unittest.makeSuite( TestSolveMasyu ) )
	return suite

if __name__=="__main__":
	unittest.main()
