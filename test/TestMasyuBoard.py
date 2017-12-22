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
		self.assertEquals( self.masyuBoard.getValue( 2, 0 ), ( "b", 0 ) )
	def test_getValue_bottomRight( self ):
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertEquals( self.masyuBoard.getValue( 2, 2 ), ( ".", 0 ) )
	def test_Print_type( self ):
		""" fails if not string """
		self.masyuBoard.initBoard( 3 )
		self.assertEquals( type( self.masyuBoard.__str__() ), type( "" ), "Should return a string" )
	def test_Print_value( self ):
		""" string shows board """
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.assertEquals( self.masyuBoard.__str__(), ".wb\n...\nb.." )
	def test_setValue_goodRange_black( self ):
		self.masyuBoard.setValue( 0, 0, "b" )
		self.assertEquals( self.masyuBoard.getValue( 0, 0 ), ( "b", 0 ) )
	def test_setValue_goodRange_white( self ):
		self.masyuBoard.setValue( 1, 0, "w" )
		self.assertEquals( self.masyuBoard.getValue( 1, 0 ), ( "w", 0 ) )
	def test_setValue_goodRange_empty_null( self ):
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.masyuBoard.setValue( 2, 0 )
		self.assertEquals( self.masyuBoard.getValue( 2, 0 ), ( ".", 0 ) )
	def test_setValue_goodRange_empty_period( self ):
		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
		self.masyuBoard.setValue( 2, 0, "." )
		self.assertEquals( self.masyuBoard.getValue( 2, 0 ), ( ".", 0 ) )
	def test_setValue_outsideRange_xHigh( self ):
		self.assertRaises( ValueError, self.masyuBoard.setValue, 3, 0, "b" )
	def test_setValue_outsideRange_yHigh( self ):
		self.assertRaises( ValueError, self.masyuBoard.setValue, 0, 3, "b" )


def suite():
	suite = unittest.TestSuite()
	suite.addTests( unittest.makeSuite( TestMasyuBoard ) )
	return suite

if __name__=="__main__":
	unittest.main()
