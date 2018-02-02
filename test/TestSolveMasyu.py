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
		self.assertFalse( self.Masyu.dot( 0, 0 ) )
	def test_Masyu_dot_black( self ):
		self.assertTrue( self.Masyu.dot( 2, 0 ) )
	def test_Masyu_dot_white( self ):
		self.assertTrue( self.Masyu.dot( 1, 0 ) )
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
	def test_Masyu_blackDot_falseOnSolved( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_00.txt" )
		self.Masyu.dotBlack( 2, 0 )
		self.assertFalse( self.Masyu.dotBlack( 2, 0 ) )
	def test_Masyu_blackDot_falseOnUnableToSolve( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_5x5_single_black.txt" )
		self.Masyu.dotBlack( 1, 2 )
		self.assertFalse( self.Masyu.dotBlack( 1, 2 ) )
	def test_Masyu_blackDot_sideBySide( self ):
		self.Masyu.board.initBoard( 6, 6, "..bb..\n......\n......\n......\n......\n......" )
		self.Masyu.dotBlack( 2, 0 )
		self.Masyu.dotBlack( 3, 0 )
		self.assertEquals( self.Masyu.board.getValue( 1, 0 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.WEST | self.Masyu.board.EAST ) )
	def test_Masyu_whiteDot_onTheEdge_North( self ):
		self.Masyu.dotWhite( 1, 0 )
		self.assertEquals( self.Masyu.board.getValue( 1, 0 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.WEST | self.Masyu.board.EAST ) )
	def test_Masyu_whiteDot_hasEntryLine( self ):
		self.Masyu.board.initBoard( 4, 3, "....\n.ww.\n...." )
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.EAST )
		self.Masyu.dotWhite( 1, 1 )
		self.assertEquals( self.Masyu.board.getValue( 1, 1 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.WEST | self.Masyu.board.EAST ) )
	def test_Masyu_whiteDot_boarderedOnTwoSidesByWhiteDots( self ):
		""" a white dot in the middle of 2 others cannot go through them.
		( only 2 white dots can be on a straight line )
		"""
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n.www.\n.....\n....." )
		self.Masyu.dotWhite( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.EAST | self.Masyu.board.WEST ) << 4 | self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) )
	def test_Masyu_empty_returns_false( self ):
		self.assertFalse( self.Masyu.dot( 1, 1 ) )
	def test_Masyu_empty_lineOnly_setsNoExits( self ):
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.EAST )
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.WEST )
		self.Masyu.dot( 1, 1 )
		self.assertEquals( self.Masyu.board.getValue( 1, 1 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.EAST | self.Masyu.board.WEST ) )
	def test_Masyu_empty_lineOnly_returns_True( self ):
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.EAST )
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.WEST )
		self.assertTrue( self.Masyu.dot( 1, 1 ) )
	def test_Masyu_empty_lineAndNoExits_returnsFalse( self ):
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.EAST )
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.WEST )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.NORTH )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.SOUTH )
		self.assertFalse( self.Masyu.dot( 1, 1 ) )
	def test_Masyu_empty_singleEntry_singleExit_EastToWest( self ):
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.EAST )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.NORTH )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.SOUTH )
		self.Masyu.dot( 1, 1 )
		self.assertEquals( self.Masyu.board.getValue( 1, 1 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.EAST | self.Masyu.board.WEST ) )
	def test_Masyu_empty_singleEntry_singleExit_WestToEast( self ):
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.WEST )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.NORTH )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.SOUTH )
		self.Masyu.dot( 1, 1 )
		self.assertEquals( self.Masyu.board.getValue( 1, 1 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.EAST | self.Masyu.board.WEST ) )
	def test_Masyu_empty_singleEntry_singleExit_NorthToEast( self ):
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.NORTH )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.WEST )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.SOUTH )
		self.Masyu.dot( 1, 1 )
		self.assertEquals( self.Masyu.board.getValue( 1, 1 )[1],
				( ( self.Masyu.board.WEST | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.EAST | self.Masyu.board.NORTH ) )
	def test_Masyu_empty_singleEntry_singleExit_EastToSouth( self ):
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.EAST )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.NORTH )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.WEST )
		self.Masyu.dot( 1, 1 )
		self.assertEquals( self.Masyu.board.getValue( 1, 1 )[1],
				( ( self.Masyu.board.WEST | self.Masyu.board.NORTH ) << 4 | self.Masyu.board.EAST | self.Masyu.board.SOUTH ) )
	def test_Masyu_empty_singleEntry_singleExit_SouthToWest( self ):
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.WEST )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.NORTH )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.EAST )
		self.Masyu.dot( 1, 1 )
		self.assertEquals( self.Masyu.board.getValue( 1, 1 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.EAST ) << 4 | self.Masyu.board.SOUTH | self.Masyu.board.WEST ) )
	def test_Masyu_empty_singleEntry_singleExit_WestToNorth( self ):
		self.Masyu.board.setExit( 1, 1, self.Masyu.board.WEST )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.EAST )
		self.Masyu.board.setNoExit( 1, 1, self.Masyu.board.SOUTH )
		self.Masyu.dot( 1, 1 )
		self.assertEquals( self.Masyu.board.getValue( 1, 1 )[1],
				( ( self.Masyu.board.EAST | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.NORTH | self.Masyu.board.WEST ) )
	def test_Masyu_empty_threeNoExits_setFourthNoExit( self ):
		""" normally corners, could be elsewhere though """
		self.Masyu.board.setNoExit( 2, 2, self.Masyu.board.WEST )
		self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( 15 << 4 ) ) )
	def test_Masyu_blackDot_ignoreDirectionWhereThereIsASingleExitAt90DegreesInTheNextCoordinate( self ):
		""" since the black dot has to go a distance of 2, a location with a single exit at 90 degrees would
		need to exclude that direction.
		invalid board... """
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n..b..\n..www\n....." )
		self.Masyu.dot( 2, 2 )
		self.Masyu.dot( 3, 3 )
		self.Masyu.dot( 4, 3 )
		self.Masyu.dot( 2, 3 )
		self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.EAST ) << 4 | self.Masyu.board.SOUTH | self.Masyu.board.WEST ) )
	def test_Masyu_whiteDot_followLine_terminateShortestEnd_01( self ):
		""" a white dot 'must turn in the previous and/or next cell in its path.'
		-w- has not enough info
		-w-.- has enough to make  x-w-.-
		-w-w- would work the same, each dot would terminate the short end  x-w-w-x
		-w-.-.-.-.-.-w- is no different.
		|-w-| would set the exits anyway
		"""
		self.Masyu.board.initBoard( 6, 2, "..ww..\n......" )
		self.Masyu.dot( 2, 0 )  # draws the first one.
		self.Masyu.dot( 3, 0 )  # draws the 2nd one.
		self.Masyu.dot( 2, 0 )  # this time it should find the noExit
		self.assertEquals( self.Masyu.board.getValue( 1, 0 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.WEST ) << 4 | self.Masyu.board.EAST ) )
	def test_Masyu_whiteDot_followLine_terminateShortestEnd_02( self ):
		self.Masyu.board.initBoard( 7, 2, "..w.w..\n......." )
		self.Masyu.dot( 2, 0 )  # draws the first one.
		self.Masyu.dot( 4, 0 )  # draws the 2nd one.
		self.Masyu.dot( 2, 0 )
		self.assertEquals( self.Masyu.board.getValue( 1, 0 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.WEST ) << 4 | self.Masyu.board.EAST ) )
		self.Masyu.dot( 4, 0 )
		self.assertEquals( self.Masyu.board.getValue( 5, 0 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.EAST ) << 4 | self.Masyu.board.WEST ) )
	def test_Masyu_followLine_01( self ):
		self.Masyu.board.initBoard( 4, 5, "....\n....\n....\n....\n...." )
		self.Masyu.board.setExit( 0, 0, self.Masyu.board.EAST )
		self.Masyu.board.setExit( 0, 0, self.Masyu.board.SOUTH )
		self.Masyu.board.setExit( 1, 0, self.Masyu.board.SOUTH )
		result = self.Masyu.followLine( 0, 1 )
		self.assertEquals( result, ( 1, 1 ) )
	def test_Masyu_line_cannotCreateSmallLoop( self ):
		self.Masyu.board.initBoard( 4, 5, "....\n.www\n....\n....\n...." )
		self.Masyu.solveBoard()
		self.assertEquals( self.Masyu.board.getValue( 0, 3 )[1],
				( ( self.Masyu.board.WEST ) << 4 | self.Masyu.board.NORTH ) )
	def test_Masyu_blackDot_preconnected_lines_setsNoExits_01( self ):
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n..b..\n.....\n....." )
		self.Masyu.board.setExit( 2, 2, self.Masyu.board.NORTH )
		self.Masyu.board.setExit( 2, 2, self.Masyu.board.EAST )
		result = self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.SOUTH | self.Masyu.board.WEST ) << 4 | self.Masyu.board.NORTH | self.Masyu.board.EAST ) )
	def test_Masyu_blackDot_preconnected_lines_setsNoExits_02( self ):
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n..b..\n.....\n....." )
		self.Masyu.board.setExit( 2, 2, self.Masyu.board.SOUTH )
		self.Masyu.board.setExit( 2, 2, self.Masyu.board.WEST )
		result = self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.EAST ) << 4 | self.Masyu.board.SOUTH | self.Masyu.board.WEST ) )
	def test_Masyu_blackDot_preconnected_lines_setsNoExits_03( self ):
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n..b..\n.....\n....." )
		self.Masyu.board.setExit( 2, 2, self.Masyu.board.SOUTH )
		self.Masyu.board.setExit( 2, 2, self.Masyu.board.WEST )
		self.Masyu.board.setNoExit( 2, 2, self.Masyu.board.NORTH )
		result = self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.EAST ) << 4 | self.Masyu.board.SOUTH | self.Masyu.board.WEST ) )
	def test_Masyu_whiteDot_TwoInLineWithLineinline_lineInWest( self ):
		""" -.ww   Testing the left white dot will result in it having a vertical line.
		"""
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n..ww.\n.....\n....." )
		self.Masyu.board.setExit( 1, 2, self.Masyu.board.WEST )
		self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.EAST | self.Masyu.board.WEST ) << 4 | self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) )
	def test_Masyu_whiteDot_TwoInLineWithLineinline_lineInEast( self ):
		""" .ww.-   Testing the left white dot will result in it having a vertical line.
		"""
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n.ww..\n.....\n....." )
		self.Masyu.board.setExit( 3, 2, self.Masyu.board.EAST )
		self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.EAST | self.Masyu.board.WEST ) << 4 | self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) )
	def test_Masyu_whiteDot_TwoInLineWithLineinline_lineInNorth( self ):
		""" see other tests for this for example """
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n..w..\n..w..\n....." )
		self.Masyu.board.setExit( 2, 1, self.Masyu.board.NORTH )
		self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.EAST | self.Masyu.board.WEST ) )
	def test_Masyu_whiteDot_TwoInLineWithLineinline_lineInSouth( self ):
		""" see other tests for this for example """
		self.Masyu.board.initBoard( 5, 5, ".....\n..w..\n..w..\n.....\n....." )
		self.Masyu.board.setExit( 2, 3, self.Masyu.board.SOUTH )
		self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.EAST | self.Masyu.board.WEST ) )
	def test_Masyu_whiteDot_inTheMiddleOfTwoIncomingLines_EastWest( self ):
		""" -. w .- should result in a vertical line
		-- the white dot needs to turn 90 degrees either before or after. """
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n..w..\n.....\n....." )
		self.Masyu.board.setExit( 1, 2, self.Masyu.board.WEST )
		self.Masyu.board.setExit( 3, 2, self.Masyu.board.EAST )
		self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.EAST | self.Masyu.board.WEST ) << 4 | self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) )
	def test_Masyu_whiteDot_inTheMiddleOfTwoIncomingLines_NorthSouth( self ):
		""" -. w .- """
		self.Masyu.board.initBoard( 5, 5, ".....\n.....\n..w..\n.....\n....." )
		self.Masyu.board.setExit( 2, 1, self.Masyu.board.NORTH )
		self.Masyu.board.setExit( 2, 3, self.Masyu.board.SOUTH )
		self.Masyu.dot( 2, 2 )
		self.assertEquals( self.Masyu.board.getValue( 2, 2 )[1],
				( ( self.Masyu.board.NORTH | self.Masyu.board.SOUTH ) << 4 | self.Masyu.board.EAST | self.Masyu.board.WEST ) )


	def test_Masyu_SolveBoard_00( self ):
		self.Masyu.board.initBoard( 3, 3, ".w.\nw..\n..." )
		self.Masyu.solveBoard()

	def test_Masyu_SolveBoard_01( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_10x12_hard.txt" )
		self.Masyu.solveBoard()
	def test_Masyu_SolveBoard_02( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_13x15_hard_1-1-6.txt" )
		self.Masyu.solveBoard()
	def test_Masyu_SolveBoard_02( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_13x15_hard_1-1-7.txt" )
		self.Masyu.solveBoard()
	def test_Masyu_SolveBoard_03( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_6x6_easy_1-1-3.txt" )
		self.Masyu.solveBoard()
	def test_Masyu_SolveBoard_04( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_13x15_hard_1-3-7.txt" )
		self.Masyu.solveBoard()
	def test_Masyu_SolveBoard_05( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_6x6_easy_example.txt" )
		self.Masyu.solveBoard()
	def test_Masyu_SolveBoard_06( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_13x15_medium_1-1-1.txt" )
		self.Masyu.solveBoard()
	def test_Masyu_SolveBoard_07( self ):
		self.Masyu.board.loadFromFile( "puzzles/puzzle_17x17_01.txt" )
		self.Masyu.solveBoard()

def suite():
	suite = unittest.TestSuite()
	suite.addTests( unittest.makeSuite( TestSolveMasyu ) )
	return suite

if __name__=="__main__":
	unittest.main()
