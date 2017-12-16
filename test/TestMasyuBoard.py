import unittest
from MasyuBoard import *

class TestMasyuBoard(unittest.TestCase):
	def setUp( self ):
		""" setUp - create a Masyu board """
		self.masyuBoard = MasyuBoard()
		#self.myBoard = SudokuBoard(9)
		#self.myBoard.initBoard( "5,,,,6,,7,,,,,,,7,8,,1,3,7,,9,5,,,6,8,,,9,,,,3,1,,5,3,,,8,,6,,,4,4,,5,7,,,,6,,,5,2,,,7,4,,6,8,6,,4,9,,,,,,,4,,2,,8,,7" )
		#self.myBoard.loadFromFile("sudokuboard.puzzle.test")
		pass
	def test_initBoard_01( self ):
		""" initBoard with a blank puzzle, size """
		self.masyuBoard.initBoard( 3 )
	def test_initBoard_02( self ):
		""" initBoard with a blank puzzle, string """
		self.masyuBoard.initBoard( "...\n...\n..." )
	def test_initBoard_03( self ):
		""" initBoard from a file """
		#self.masyuBoard.loadFromFile("puzzles/puzzle_2.txt")
		pass

def suite():
	suite = unittest.TestSuite()
	suite.addTests( unittest.makeSuite( TestMasyuBoard ) )
	return suite

if __name__=="__main__":
	unittest.main()
