#########################################
# Project:    Masyu Solver
# Filename:   MasyuBoard.py
# Author:     Opussf
# Started:    16 Dec 2017
#########################################

import math

class MasyuBoard( object ):
	"""Masyu Board object
	dotBoard is a single list that holds the initial board.  The dots are placed here.
	lineBoard is a single list that holds the values for the lines.
		A line is defined as an 8 bit value of entry / exit points, and unavailable exit / entry points.
		(not) nesw << 4 + nesw

	"""
	NORTH = 1
	EAST  = 2
	SOUTH = 4
	WEST  = 8
	dirValues = { 'w': WEST, 's': SOUTH, 'e': EAST, 'n': NORTH }
	dirLetters = dirValues.keys()
	def __init__( self, debug=False ):
		self.debug = debug
	def initBoard( self, xSize=None, ySize=None, line=None ):
		""" init the board,
		xSize @parameter (int or None): xSize of the puzzle.
		ySize @parameter (int or None): ySize of the puzzle. Try to guess this if not given.
		line @parameter (string or None): line to init puzzle with. Line needs to be broken with line feeds.

		if line is given, and no sizes, try to guess at the x,y size of the puzzle
		"""
		if self.debug:
			print( ">>>(xSize, ySize) (%s,%s) line: %s" % ( xSize or "None", ySize or "None", line or "None" ) )

		if line:
			brokenLine = line.split("\n")
			self.ySize = len( brokenLine )
			self.xSize = len( brokenLine[0] )

			if( self.xSize * self.ySize != len( "".join( brokenLine ) ) ):
				print( "Problem child?" )
		else:
			self.xSize = xSize
			self.ySize = ySize or xSize
#		if self.debug:
#			print( ":: (xSize, ySize) (%s,%s) line: %s" % ( self.xSize or "None", self.ySize or "None", line or "None" ) )
		self.baseBoard = ["."] * ( self.xSize * self.ySize )
		self.lineBoard = [0b00000000] * ( self.xSize * self.ySize )

		if line:
			self.baseBoard = [ brokenLine[y][x] for y in range(self.ySize) for x in range(self.xSize) ]
		if self.debug:
			print self.baseBoard
	def loadFromFile( self, puzzleFile ):
		""" reads a puzzle file, and inits the board """
		puzzle = file( puzzleFile, "r" ).read()
		self.initBoard( line=puzzle )
	def __offset( self, x, y ):
		""" private function.  return the offset, or raise a valueerror """
		if( x >= self.xSize or y >= self.ySize ):
			raise( ValueError )
		return( y*self.xSize + x )
	def __str__( self ):
		#yaya = [ [ self.baseBoard[] ] ]
		out = [ [ self.baseBoard[y*self.xSize + x] for x in range(self.xSize)] for y in range(self.ySize) ]
		out = map( "".join, out )
		return "\n".join( out )
	def getValue( self, x, y ):
		""" returns a tuple of the base and line boards """
		offset = self.__offset( x, y )
#		if( x >= self.xSize or y >= self.ySize ):
#			raise( ValueError )
#		offset = y*self.xSize + x
		return( (self.baseBoard[offset], self.lineBoard[offset]) )
	def setValue( self, x, y, value=None ):
		""" sets a value """
		offset = self.__offset( x, y )
		if( value == None ):
			value = "."
		self.baseBoard[offset] = value
	def setExit( self, x, y, value=None ):
		""" sets the exit flag for value direction.
		value @parameter (binary, single char, None) value to set.
		"""
		offset = self.__offset( x, y )
		if( isinstance( value, str ) ):
			#print "value is str"
			value = value.lower()
			if( value[0] in self.dirLetters ):
				value = self.dirValues[value[0]]
			else:
				raise( ValueError )
		if( value < 0 or value > 15 ):
			raise( ValueError )
		self.lineBoard[offset] = self.lineBoard[offset] | value

