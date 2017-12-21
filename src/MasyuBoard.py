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
	def __init__( self, debug=False ):
		self.debug = debug
#		self.NORTH = 1
#		self.EAST  = 2
#		self.SOUTH = 4
#		self.WEST  = 8

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
	def __str__( self ):
		#yaya = [ [ self.baseBoard[] ] ]
		out = [ [ self.baseBoard[y*self.xSize + x] for x in range(self.xSize)] for y in range(self.ySize) ]
		out = map( "".join, out )
		return "\n".join( out )
	def getValue( self, x, y ):
		""" returns a tuple of the base and line boards """
		if( x >= self.xSize  or y >= self.ySize ):
			raise( ValueError )
		offset = y*self.xSize + x
		return( (self.baseBoard[offset], self.lineBoard[offset]) )
