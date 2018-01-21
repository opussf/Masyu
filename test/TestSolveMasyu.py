import unittest
from MasyuBoard import *
from SolveMasyu import *

class TestSolveMasyu( unittest.TestCase ):
	Masyu = SolveMasyu( MasyuBoard.MasyuBoard() )
	def setUp( self ):
		""" setUp """
		self.Masyu.board.loadFromFile( "puzzles/puzzle_0.txt" )
	def test_Masyu_hasBoard( self ):
		self.assertTrue( self.Masyu.board )
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

	def test_Masyu_blackDot_vertical_02( self ):
		self.Masyu.dotBlack( 2, 0 )
		self.assertEquals( self.Masyu.board.getValue( 0, 0 )[1],
				( self.Masyu.board.NORTH | self.Masyu.board.WEST ) << 4 | self.Masyu.board.EAST )
	def test_Masyu_blackDot_horizontal_02( self ):
		self.Masyu.dotBlack( 0, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( self.Masyu.board.SOUTH | self.Masyu.board.EAST ) << 4 | self.Masyu.board.WEST )
	def test_Masyu_blackDot_single_exit_East( self ):
		""" draws the one line it can guess at """
		self.Masyu.board.loadFromFile( "puzzles/puzzle_5x5_single_black.txt" )
		self.Masyu.dotBlack( 1, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.EAST | self.Masyu.board.WEST )
	def test_Masyu_blackDot_single_noExit_West( self ):
		""" marks a noExit on the short side """
		self.Masyu.board.loadFromFile( "puzzles/puzzle_5x5_single_black.txt" )
		self.Masyu.dotBlack( 1, 2 )
		self.assertEquals( self.Masyu.board.getValue( 1, 2 )[1],
				( self.Masyu.board.WEST << 4 ) | self.Masyu.board.EAST )
	def test_Masyu_blackDot_single_exit_West( self ):
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n...b.\n.....\n....." )
		self.Masyu.dotBlack( 3, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.EAST | self.Masyu.board.WEST )
	def test_Masyu_blackDot_single_noExit_East( self ):
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n...b.\n.....\n....." )
		self.Masyu.dotBlack( 3, 2 )
		self.assertEquals( self.Masyu.board.getValue( 3, 2 )[1],
				( self.Masyu.board.EAST << 4 | self.Masyu.board.WEST ) )
	def test_Masyu_blackDot_single_exit_South( self ):
		self.Masyu.board.initBoard( 5, 5, ".....\n..b..\n.....\n.....\n....." )
		self.Masyu.dotBlack( 2, 1 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( self.Masyu.board.EAST | self.Masyu.board.WEST ) << 4 | self.Masyu.board.NORTH | self.Masyu.board.SOUTH )
	def test_Masyu_blackDot_single_noExit_North( self ):
		self.Masyu.board.initBoard( 5, 5, ".....\n..b..\n.....\n.....\n....." )
		self.Masyu.dotBlack( 2, 1 )
		self.assertEquals( self.Masyu.board.getValue( 2, 1 )[1],
				( self.Masyu.board.NORTH << 4 | self.Masyu.board.SOUTH ) )
	def test_Masyu_blackDot_single_exit_North( self ):
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n.....\n..b..\n....." )
		self.Masyu.dotBlack( 2, 3 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( self.Masyu.board.EAST | self.Masyu.board.WEST ) << 4 | self.Masyu.board.NORTH | self.Masyu.board.SOUTH )
	def test_Masyu_blackDot_single_noExit_South( self ):
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n.....\n..b..\n....." )
		self.Masyu.dotBlack( 2, 3 )
		self.assertEquals( self.Masyu.board.getValue( 2, 3 )[1],
				( self.Masyu.board.SOUTH << 4 | self.Masyu.board.NORTH ) )
	def test_Masyu_blackDot_nested( self ):
		self.Masyu.board.initBoard( 5, 5, ".....\n...b.\n..b..\n.....\n....." )
		self.Masyu.dotBlack( 3, 1 )
		self.Masyu.dotBlack( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 0, 2 )[1],
				( self.Masyu.board.WEST << 4 | self.Masyu.board.EAST ) )


	def test_Masyu_SolveBoard( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_10x12_hard.txt" )
		self.Masyu.solveBoard()


"""
	def test_Masyu_blackDot_( self ):
		print "balckDot_"
		self.Masyu.board.loadFromFile( "puzzles/puzzle_5x5_single_black.txt" )
		self.Masyu.dotBlack( 2, 2 )
	def test_Masyu_solveBoard( self ):
		self.Masyu.solveBoard()
"""

def suite():
	suite = unittest.TestSuite()
	suite.addTests( unittest.makeSuite( TestSolveMasyu ) )
	return suite

if __name__=="__main__":
	unittest.main()
