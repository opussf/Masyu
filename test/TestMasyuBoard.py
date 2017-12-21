import unittest
from MasyuBoard import *

class TestMasyuBoard(unittest.TestCase):
	def setUp( self ):
		""" setUp - create a Masyu board """
		self.masyuBoard = MasyuBoard( True )
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

#	def test_initBoard_03( self ):
#		""" initBoard from a file """
#		self.masyuBoard.loadFromFile( "puzzles/puzzle_0.txt" )
#		self.assertEquals( len( self.masyuBoard.baseBoard ), 9 )
#	def test_Print(self):
#		""" fails if not string """
#		self.assertEquals( type( self.masyuBoard.__str__() ), type( "" ), "Should return a string" )

def suite():
	suite = unittest.TestSuite()
	suite.addTests( unittest.makeSuite( TestMasyuBoard ) )
	return suite

if __name__=="__main__":
	unittest.main()
