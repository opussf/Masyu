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
	def test_Masyu_solveBoard( self ):
		self.Masyu.solveBoard()
	def test_Masyu_dot_empty( self ):
		self.assertEquals( self.Masyu.dot( 0, 0 ), "empty" )
	def test_Masyu_dot_black( self ):
		self.assertEquals( self.Masyu.dot( 2, 0 ), "black" )
	def test_Masyu_dot_white( self ):
		self.assertEquals( self.Masyu.dot( 1, 0 ), "white" )

	def test_Masyu_blackDot_vertical_01( self ):
		""" finds a vertical component """
		self.Masyu.dotBlack( 0, 2 )
		self.assertEquals( self.Masyu.board.getValue( 0, 0 )[1],
				( self.Masyu.board.NORTH | self.Masyu.board.WEST ) << 4 | self.Masyu.board.SOUTH )
	def test_Masyu_blackDot_horizontal_01( self ):
		""" find a horizontal component """
		self.Masyu.dotBlack( 0, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( self.Masyu.board.SOUTH | self.Masyu.board.EAST ) << 4 | self.Masyu.board.WEST )
	def test_Masyu_blackDot_( self ):
		pass
		#self.fail( "Eh?" )
"""
	def test_Masyu_blackDot_( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_5x5_single_black.txt" )
		self.Masyu.dotBlack( 2, 2 )


def suite():
	suite = unittest.TestSuite()
	suite.addTests( unittest.makeSuite( TestSolveMasyu ) )
	return suite

if __name__=="__main__":
	unittest.main()
