import unittest
from MasyuBoard import *

class TestMasyuBoard(unittest.TestCase):
	def setUp(self):
		""" setUP - create a 9x9 board, and load from puzzles.txt """
		#self.myBoard = SudokuBoard(9)
		#self.myBoard.initBoard( "5,,,,6,,7,,,,,,,7,8,,1,3,7,,9,5,,,6,8,,,9,,,,3,1,,5,3,,,8,,6,,,4,4,,5,7,,,,6,,,5,2,,,7,4,,6,8,6,,4,9,,,,,,,4,,2,,8,,7" )
		#self.myBoard.loadFromFile("sudokuboard.puzzle.test")
		pass
	def test_initBoard_01( self ):
		""" initBoard with a blank string """
		#self.myBoard.initBoard( "" )
		pass

def suite():
	suite = unittest.TestSuite()
	suite.addTests( unittest.makeSuite( TestMasyuBoard ) )
	return suite

if __name__=="__main__":
	unittest.main()
