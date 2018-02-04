import unittest
from MasyuBoard import *

class TestMasyuBoard( unittest.TestCase ):
	def setUp( self ):
		""" setUp - create a Masyu board """
		self.masyuBoard = MasyuBoard( False )
	def test_initBoard_singleDimension_named( self ):
		""" initBoard with a blank puzzle, size.  Create a square puzzle """
		self.masyuBoard.initBoard( xSize=3 )
		self.assertEquals( len( self.masyuBoard.baseBoard ), 9 )
	def test_initBoard_singleDimension_position( self ):
		""" initBoard with a blank puzzle, size.  Create a square puzzle """
		self.masyuBoard.initBoard( 3 )
		self.assertEquals( len( self.masyuBoard.baseBoard ), 9 )
	def test_initBoard_cannotInitTooSmall( self ):
		""" the smallest Masyu board is 3x3. """
		self.assertRaises( ValueError, self.masyuBoard.initBoard, 2 )
	def test_initBoard_dualDimension_named( self ):
		""" initBoard with a blank puzzle, 2 sizes.  Allows a non-square puzzle. """
		self.masyuBoard.initBoard( xSize=4, ySize=3 )
		self.assertEquals( len( self.masyuBoard.baseBoard ), 12 )
		self.assertEquals( self.masyuBoard.xSize, 4 )
		self.assertEquals( self.masyuBoard.ySize, 3 )
	def test_initBoard_dualDimension_position( self ):
		""" initBoard with a blank puzzle, 2 sizes.  Allows a non-square puzzle. """
		self.masyuBoard.initBoard( 4, 3 )
		self.assertEquals( len( self.masyuBoard.baseBoard ), 12 )
		self.assertEquals( self.masyuBoard.xSize, 4 )
		self.assertEquals( self.masyuBoard.ySize, 3 )
	def test_initBoard_string_linefeeds_named( self ):
		""" initBoard with a blank puzzle, string, with linefeeds """
		self.masyuBoard.initBoard( line="...\n...\n..." )
		self.assertEquals( len( self.masyuBoard.baseBoard ), 9 )
		self.assertEquals( self.masyuBoard.xSize, 3 )
	def test_initBoard_string_linefeeds_rectangleWide( self ):
		""" initBoard with a blank puzzle, string, with linefeeds """
		self.masyuBoard.initBoard( line="....\n....\n...." )
		self.assertEquals( len( self.masyuBoard.baseBoard ), 12 )
		self.assertEquals( self.masyuBoard.xSize, 4 )
		self.assertEquals( self.masyuBoard.ySize, 3 )
	def test_initBoard_string_linefeeds_rectangleTall( self ):
		""" initBoard with a blank puzzle, string, with linefeeds """
		self.masyuBoard.initBoard( line="...\n...\n...\n..." )
		self.assertEquals( len( self.masyuBoard.baseBoard ), 12 )
		self.assertEquals( self.masyuBoard.xSize, 3 )
		self.assertEquals( self.masyuBoard.ySize, 4 )
	def notest_initBoard_string_linefeeds_oddSize( self ):
		""" @todo: decide if this is needed / fix / make work """
		""" initBoard with a blank puzzle, string, with linefeeds """
		self.masyuBoard.initBoard( line="....\n...\n...\n..." )
		self.assertEquals( len( self.masyuBoard.baseBoard ), 12 )
		self.assertEquals( self.masyuBoard.xSize, 3 )
		self.assertEquals( self.masyuBoard.ySize, 4 )
	def test_initBoard_fromFile( self ):
		""" read puzzle from file """
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertEquals( len( self.masyuBoard.baseBoard ), 9 )
		self.assertEquals( self.masyuBoard.baseBoard[2], "b" )
	def test_getValue_outsideRange_xHigh( self ):
		""" x value is too high (out of range) """
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertRaises( ValueError, self.masyuBoard.getValue, 3, 0 )
	def test_getValue_outsideRange_yHigh( self ):
		""" y value is too high (out of range) """
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertRaises( ValueError, self.masyuBoard.getValue, 0, 3 )
	def test_getValue_topRight( self ):
		""" getValue returns a tuple. no lines made """
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertEquals( self.masyuBoard.getValue( 2, 0 ), ( "b", 48 ) )
	def test_getValue_bottomRight( self ):
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertEquals( self.masyuBoard.getValue( 2, 2 ), ( ".", 96 ) )
	def test_Print_type( self ):
		""" fails if not string """
		self.masyuBoard.initBoard( 3 )
		self.assertEquals( type( self.masyuBoard.__str__() ), type( "" ), "Should return a string" )
	def test_Print_value( self ):
		""" string shows board """
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertEquals( self.masyuBoard.__str__(), ". w b\n     \n. . .\n     \nb . ." )
	def test_setValue_goodRange_black( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setValue( 0, 0, "b" )
		self.assertEquals( self.masyuBoard.getValue( 0, 0 ), ( "b", 144 ) )
	def test_setValue_goodRange_white( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setValue( 1, 0, "w" )
		self.assertEquals( self.masyuBoard.getValue( 1, 0 ), ( "w", 16 ) )
	def test_setValue_goodRange_empty_null( self ):
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.masyuBoard.setValue( 2, 0 )
		self.assertEquals( self.masyuBoard.getValue( 2, 0 ), ( ".", 48 ) )
	def test_setValue_goodRange_empty_period( self ):
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.masyuBoard.setValue( 2, 0, "." )
		self.assertEquals( self.masyuBoard.getValue( 2, 0 ), ( ".", 48 ) )
	def test_setValue_outsideRange_xHigh( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setValue, 3, 0, "b" )
	def test_setValue_outsideRange_yHigh( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setValue, 0, 3, "b" )
	def test_setExit_goodRange_single( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 2, 0, 'w' )
		self.assertEquals( self.masyuBoard.lineBoard[2],
				( self.masyuBoard.NORTH | self.masyuBoard.EAST ) << 4 | self.masyuBoard.WEST )
	def test_setExit_goodRange_multiple( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 2, 0, 'w' )
		self.masyuBoard.setExit( 2, 0, 's' )
		self.assertEquals( self.masyuBoard.lineBoard[2],
				( self.masyuBoard.NORTH | self.masyuBoard.EAST ) << 4 | self.masyuBoard.WEST | self.masyuBoard.SOUTH )
	def test_setExit_outsideRange_xHigh( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setExit, 0, 3, "n" )
	def test_setExit_outsideRange_yHigh( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setExit, 0, 3, "n" )
	def test_setExit_takesLetter( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 0, 0, "s" )
		self.assertEquals( self.masyuBoard.lineBoard[0],
				( self.masyuBoard.NORTH | self.masyuBoard.WEST ) << 4 | self.masyuBoard.SOUTH )
	def test_setExit_secondLetterIsIgnored( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 0, 0, "se" )
		self.assertEquals( self.masyuBoard.lineBoard[0],
				( self.masyuBoard.NORTH | self.masyuBoard.WEST ) << 4 | self.masyuBoard.SOUTH )
	def test_setExit_invalidLetter( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setExit, 0, 0, "z" )
	def test_setExit_uppercaseLetter( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 0, 0, "S" )
		self.assertEquals( self.masyuBoard.lineBoard[0], ( self.masyuBoard.NORTH | self.masyuBoard.WEST ) << 4 | self.masyuBoard.SOUTH )
	def test_setExit_takesNumber( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 0, 0, self.masyuBoard.EAST )
		self.assertEquals( self.masyuBoard.lineBoard[0],
				( self.masyuBoard.NORTH | self.masyuBoard.WEST ) << 4 | self.masyuBoard.EAST )
	def test_setExit_takesNumber_complex( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 0, 0, self.masyuBoard.EAST | self.masyuBoard.SOUTH )
		self.assertEquals( self.masyuBoard.lineBoard[0],
				( self.masyuBoard.NORTH | self.masyuBoard.WEST ) << 4 | self.masyuBoard.EAST | self.masyuBoard.SOUTH )
	def test_setExit_takesNumber_invalid( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setExit, 0, 0, 16 )
	def test_setExit_exitsBoard_north( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setExit, 0, 0, self.masyuBoard.NORTH )
	def test_setExit_exitsBoard_south( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setExit, 2, 2, self.masyuBoard.SOUTH )
	def test_setExit_exitsBoard_east( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setExit, 2, 2, self.masyuBoard.EAST )
	def test_setExit_exitsBoard_west( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setExit, 0, 0, self.masyuBoard.WEST )
	def test_setExit_exitsBoard_2values( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setExit, 2, 0, self.masyuBoard.EAST | self.masyuBoard.NORTH )
	def test_setExit_setsExitForNextLocation_north( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 1, 1, self.masyuBoard.NORTH )
		self.assertEquals( self.masyuBoard.lineBoard[1],
				( self.masyuBoard.NORTH << 4 | self.masyuBoard.SOUTH ) )
	def test_setExit_setsExitForNextLocation_south( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 1, 1, self.masyuBoard.SOUTH )
		self.assertEquals( self.masyuBoard.lineBoard[7],
				( self.masyuBoard.SOUTH << 4 | self.masyuBoard.NORTH ) )
	def test_setExit_setsExitForNextLocation_east( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 1, 1, self.masyuBoard.EAST )
		self.assertEquals( self.masyuBoard.lineBoard[5],
				( self.masyuBoard.EAST << 4 | self.masyuBoard.WEST ) )
	def test_setExit_setsExitForNextLocation_west( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 1, 1, self.masyuBoard.WEST )
		self.assertEquals( self.masyuBoard.lineBoard[3],
				( self.masyuBoard.WEST << 4 | self.masyuBoard.EAST ) )
	def test_Print_showsLine( self ):
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.masyuBoard.setExit( 2, 0, 'w' )
		self.masyuBoard.setExit( 2, 0, 's' )
		#self.assertEquals( self.masyuBoard.__str__(), u". w\u2500b\n    \u2502\n. . .\n     \nb . ." )
		self.assertEquals( self.masyuBoard.__str__(), u". w-b\n    |\n. . .\n     \nb . ." )
	def test_Print_completed_puzzle( self ):
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.masyuBoard.setExit( 1, 0, self.masyuBoard.EAST | self.masyuBoard.WEST )
		self.masyuBoard.setExit( 2, 0, "s" )
		self.masyuBoard.setExit( 2, 1, "s" )
		self.masyuBoard.setExit( 0, 2, self.masyuBoard.NORTH | self.masyuBoard.EAST )
		self.masyuBoard.setExit( 0, 1, "n" )
		self.masyuBoard.setExit( 1, 2, "e" )
		self.assertEquals( self.masyuBoard.__str__(), ".-w-b\n|   |\n. . .\n|   |\nb-.-." )
	def test_setNoExit_goodRange_single( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setNoExit( 1, 1, "n" )
		self.assertEquals( self.masyuBoard.lineBoard[4], self.masyuBoard.NORTH << 4 )
	def test_setNoExit_invalidLetter( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setNoExit, 0, 0, "z" )
	def test_setNoExit_takesNumber_invalid( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertRaises( ValueError, self.masyuBoard.setNoExit, 0, 0, 16 )
	def test_setNoExit_setsNoExitForNextLocation_north( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setNoExit( 1, 1, self.masyuBoard.NORTH )
		self.assertEquals( self.masyuBoard.lineBoard[1], ( self.masyuBoard.NORTH | self.masyuBoard.SOUTH ) << 4 )
	def test_setNoExit_setsNoExitForNextLocation_south( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setNoExit( 1, 1, self.masyuBoard.SOUTH )
		self.assertEquals( self.masyuBoard.lineBoard[7], ( self.masyuBoard.SOUTH | self.masyuBoard.NORTH ) << 4 )
	def test_setNoExit_setsNoExitForNextLocation_east( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setNoExit( 1, 1, self.masyuBoard.EAST )
		self.assertEquals( self.masyuBoard.lineBoard[5], ( self.masyuBoard.EAST | self.masyuBoard.WEST ) << 4 )
	def test_setNoExit_setsNoExitForNextLocation_west( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setNoExit( 1, 1, self.masyuBoard.WEST )
		self.assertEquals( self.masyuBoard.lineBoard[3], ( self.masyuBoard.WEST | self.masyuBoard.EAST ) << 4 )
	def test_setNoExit_doesNotChangeExit( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 1, 1, self.masyuBoard.EAST | self.masyuBoard.WEST )  # exit is e-w
		self.masyuBoard.setNoExit( 1, 1, self.masyuBoard.NORTH | self.masyuBoard.SOUTH )
		expectedValue = (self.masyuBoard.NORTH | self.masyuBoard.SOUTH) << 4
		expectedValue = expectedValue | self.masyuBoard.EAST | self.masyuBoard.WEST
		self.assertEquals( expectedValue, self.masyuBoard.lineBoard[4] )
	def test_setExit_doesNotChangeNoExit( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setNoExit( 1, 1, self.masyuBoard.EAST | self.masyuBoard.WEST ) # don't exit east or west
		self.masyuBoard.setExit( 1, 1, self.masyuBoard.NORTH | self.masyuBoard.SOUTH )

		expectedValue = (self.masyuBoard.EAST | self.masyuBoard.WEST) << 4
		expectedValue = expectedValue | self.masyuBoard.NORTH | self.masyuBoard.SOUTH
		self.assertEquals( expectedValue, self.masyuBoard.lineBoard[4] )
	def test_setNoExit_doesNotErrorOnSettingNoExitOnEdge_north( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setNoExit( 1, 0, "n" )
		self.assertEquals( self.masyuBoard.NORTH << 4, self.masyuBoard.lineBoard[1] )
	def test_initBoard_noExit_Border_NorthWest( self ):
		self.masyuBoard.initBoard( 4 )
		self.assertEquals( ( self.masyuBoard.NORTH | self.masyuBoard.WEST ) << 4, self.masyuBoard.getValue( 0, 0 )[1] )
	def test_initBoard_noExit_Border_SouthEast( self ):
		self.masyuBoard.initBoard( 4 )
		self.assertEquals( ( self.masyuBoard.SOUTH | self.masyuBoard.EAST ) << 4, self.masyuBoard.getValue( 3, 3 )[1] )
	def test_loadFromFile_savesFilename( self ):
		puzzleName = "puzzles/puzzle_17x17_01.txt"
		self.masyuBoard.loadFromFile( puzzleName )
		self.assertEquals( self.masyuBoard.filename, puzzleName )
	def test_isSolved_returnsFalse_3x3( self ):
		""" assert that isSolved returns false for an empty board """
		self.masyuBoard.initBoard( 3 )
		self.assertFalse( self.masyuBoard.isSolved() )
	def notest_isSolved_returnsTrue_3x3( self ):
		""" fix this """
		self.masyuBoard.initBoard( 3 )
		self.assertTrue( self.masyuBoard.isSolved() )
	def test_solvedPercent_3x3_00( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertEquals( self.masyuBoard.solvedPercent(), 0 )
	def test_solvedPerent_3x3_( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setExit( 0, 0, self.masyuBoard.SOUTH )
		self.masyuBoard.setExit( 0, 0, self.masyuBoard.EAST )
		self.assertEquals( self.masyuBoard.solvedPercent(), 11.11 )
	def test_getDotCount_0( self ):
		""" return how many dots are in the puzzle """
		self.masyuBoard.initBoard( 3 )
		self.assertEquals( self.masyuBoard.getDotCount()[0], 0 )
	def test_getDotCount_total( self ):
		""" return how many dots are in the puzzle """
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertEquals( self.masyuBoard.getDotCount()[0], 3 )
	def test_getDotCount_black( self ):
		""" return how many dots are in the puzzle """
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertEquals( self.masyuBoard.getDotCount()[1], 2 )
	def test_getDotCount_white( self ):
		""" return how many dots are in the puzzle """
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertEquals( self.masyuBoard.getDotCount()[2], 1 )
	def test_getBoardState_empty( self ):
		self.masyuBoard.initBoard( 3 )
		self.assertEquals( self.masyuBoard.getBoardState(), (['.','.','.','.','.','.','.','.','.',],[144,16,48,128,0,32,192,64,96]) )
	def test_getBoardState_loadedFromFile( self ):
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertEquals( self.masyuBoard.getBoardState(), (['.','w','b','.','.','.','b','.','.',],[144,16,48,128,0,32,192,64,96]) )
	def test_setBoardState_emptyWithLines( self ):
		self.masyuBoard.initBoard( 3 )
		self.masyuBoard.setBoardState( (['.','.','.','.','.','.','.','.','.'],[144,20,48,128,5,32,192,65,96]) )
		self.assertEquals( self.masyuBoard.getValue( 1, 1 )[1],
				( self.masyuBoard.NORTH | self.masyuBoard.SOUTH ) )

def suite():
	suite = unittest.TestSuite()
	suite.addTests( unittest.makeSuite( TestMasyuBoard ) )
	return suite

if __name__=="__main__":
	unittest.main()
