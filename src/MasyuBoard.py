#########################################
# Project:    Masyu Solver
# Filename:   MasyuBoard.py
# Author:     Opussf
# Started:    16 Dec 2017
#########################################

import math

class MasyuBoard( object ):
	"""Masyu Board object
	The Masyu board holds the puzzle (dotBoard), allows loading / saving the board to storage, prints the board to a string,
	allows interaction with the board ( setExit, setNoExit, getValue ).

	Coordinate system is 0 based.  (0,0) is the upper left (north-west) corner

	@ToDecide does this facilitate following lines?

	dotBoard is a single list that holds the initial board.  The dots are placed here.
	lineBoard is a single list that holds the values for the lines.
		A line is defined as an 8 bit value of entry / exit points, and unavailable exit / entry points.
		(not) nesw << 4 + nesw
	The minimum size of a Masyu board is 2x3 or 3x2.
		This would be solved with a single white dot in the middle of the 'long' dimension.

	"""
	NORTH = 1  # noNorth =  16
	EAST  = 2  # noEast  =  32
	SOUTH = 4  # noSouth =  64
	WEST  = 8  # noWest  = 128
	dirValues = { 'w': WEST, 's': SOUTH, 'e': EAST, 'n': NORTH }
	dirLetters = dirValues.keys()
	def __init__( self, debug=False ):
		self.debug = debug
		self.filename = ""
	def initBoard( self, xSize=None, ySize=None, line=None ):
		""" init the board,
		xSize @parameter (int or None): xSize of the puzzle.
		ySize @parameter (int or None): ySize of the puzzle. Try to guess this if not given.
		line @parameter (string or None): line to init puzzle with. Line needs to be broken with line feeds.

		if line is given, and no sizes, try to guess at the x,y size of the puzzle
		"""
		if self.debug:
			print( ">>>(xSize, ySize) (%s,%s) line: %s" % ( xSize or "None", ySize or "None", line or "None" ) )

		if line:  # a line has been passed to init the board
			brokenLine = line.split("\n")
			self.ySize = len( brokenLine )
			self.xSize = len( brokenLine[0] )

			if( self.xSize * self.ySize != len( "".join( brokenLine ) ) ):
				print( "Problem child?" )
		else:
			self.xSize = xSize
			self.ySize = ySize or xSize
		if( ( self.xSize < 2 or self.ySize < 2 ) or
				( self.xSize <= 2 and self.xSize <= 2 ) ):
			raise( ValueError )
		#		if self.debug:
		#			print( ":: (xSize, ySize) (%s,%s) line: %s" % ( self.xSize or "None", self.ySize or "None", line or "None" ) )
		self.baseBoard = ["."] * ( self.xSize * self.ySize )
		self.lineBoard = [0b00000000] * ( self.xSize * self.ySize )

		if line:
			self.baseBoard = [ brokenLine[y][x] for y in range(self.ySize) for x in range(self.xSize) ]
		if self.debug:
			print self.baseBoard

		for x in range( self.xSize ):
			self.setNoExit( x, 0, self.NORTH )
			self.setNoExit( x, self.ySize-1, self.SOUTH )
		for y in range( self.ySize ):
			self.setNoExit( 0, y, self.WEST )
			self.setNoExit( self.xSize-1, y, self.EAST )

		if self.filename:
			self.boardName = self.filename
		else:
			self.boardName = "puzzle %ix%i" % ( self.xSize, self.ySize )
		self.filename = ""


		# @TODO: set noexit flags around the edge of the board on init.
	def loadFromFile( self, puzzleFile ):
		""" reads a puzzle file, and inits the board """
		self.filename = puzzleFile
		puzzle = file( puzzleFile, "r" ).read()
		self.initBoard( line=puzzle )
		self.filename = puzzleFile
	def __offset( self, x, y ):
		""" private function.  return the offset, or raise a ValueError """
		#print( "__offset( %i, %i )" % ( x, y ) )
		if( x >= self.xSize or x < 0 or y >= self.ySize or y < 0 ):
			#print( "__offset: raise error" )
			raise( ValueError )
		return( y*self.xSize + x )
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
	def setExit( self, x, y, value=None, secondary=None ):
		""" sets the exit flag for value direction.
		value @parameter (binary, single char, None) value to set.
		secondary @parameter (boolean) False if this is the primary square, True if setting the 'extrance' to the secondary square
		"""
		#if debug: print( "setExit( %i, %i, %s )" % (x, y, value) )
		try:
			offset = self.__offset( x, y )
		except ValueError as e:
			if( not secondary ):
				raise( e )
			else:
				#print( "Found an exception during the secondary part.  Ignore it." )
				return
		if( isinstance( value, str ) ):  # did I get a string?
			#print "value is str"
			value = value.lower()
			if( value[0] in self.dirLetters ):
				value = self.dirValues[value[0]]
			else:
				raise( ValueError )
		if( value < 0 or value > 15 ):
			raise( ValueError )
		# raise exception if the value tries to exit the board.
		if( x == 0 and ( value & self.WEST ) ) or \
				( y == 0 and ( value & self.NORTH ) ) or \
				( x == self.xSize - 1 and ( value & self.EAST ) ) or \
				( y == self.ySize - 1 and ( value & self.SOUTH ) ):
			raise( ValueError )
		self.lineBoard[offset] = self.lineBoard[offset] | value
		if( not secondary ):
			if( value & self.NORTH ):  # going north
				#if debug: print( "Going NORTH. Set (%i,%i) to SOUTH" % (x, y-1) )
				self.setExit( x, y-1, self.SOUTH, True )
			elif( value & self.EAST ):
				#if debug: print( "Going EAST. Set (%i,%i) to WEST" % (x+1,y) )
				self.setExit( x+1, y, self.WEST, True )
			elif( value & self.SOUTH ):
				#if debug: print( "Going SOUTH. Set (%i,%i) to NORTH" % (x,y+1) )
				self.setExit( x, y+1, self.NORTH, True )
			elif( value & self.WEST ):
				#if debug: print( "Going WEST. Set (%i,%i) to EAST" % (x-1,y) )
				self.setExit( x-1, y, self.EAST, True )
	def setNoExit( self, x, y, value=None, secondary=None ):
		""" sets a no exit value for a square.
		value @parameter (binary, single char, None) direction to set to no exit
		secondary @parameter (boolean) False if this is the primary square, True if setting the 'no exit' to a secondary square
		"""
		try:
			offset = self.__offset( x, y )
		except ValueError as e:
			if( not secondary ):
				raise( e )
			else:
				#print( "Found an exception during the secondary part, ignore it." )
				return
		#print("setNoExit( %i, %i ) offset=%i" % ( x, y, offset ) )
		if( isinstance( value, str ) ):  # did I get a string?
			value = value.lower()
			if( value[0] in self.dirLetters ):
				value = self.dirValues[value[0]]
			else:
				raise( ValueError )
		if( value < 0 or value > 15 ):  # test before left shifting
			raise( ValueError )
		self.lineBoard[offset] = self.lineBoard[offset] | ( value << 4 )  # shift left at assignment
		if( not secondary ):
			if( value & self.NORTH ):  # don't go north
				self.setNoExit( x, y-1, self.SOUTH, True )
			elif( value & self.EAST ):  # don't go east
				self.setNoExit( x+1, y, self.WEST, True )
			elif( value & self.SOUTH ):  # don't go south
				self.setNoExit( x, y+1, self.NORTH, True )
			elif( value & self.WEST ):  # don't go west
				self.setNoExit( x-1, y, self.EAST, True )
	def isSolved( self ):
		""" return true if solved
		solved can be a few things....
		"""
		return ( reduce( lambda x,y: x and y, map( lambda x: ((x >> 4) ^ (x & 15) == 15), self.lineBoard ) ) )
	def solvedPercent( self ):
		""" return percent of the board that is solved
		"""
		totalSize = len( self.lineBoard )
		solvedCount = 0
		for val in self.lineBoard:
			if( ( val >> 4 ) ^ ( val & 15 ) == 15 ):
				solvedCount = solvedCount + 1
		return( float( "%.2f" % ( solvedCount * 100.0 / totalSize, ) ) )
	def getDotCount( self ):
		""" return the number of black and white dots
		total, black, white """
		black = len( filter( lambda x: x=="b", self.baseBoard ) )
		white = len( filter( lambda x: x=="w", self.baseBoard ) )
		return( ( black+white, black, white ) )
	def getBoardState( self ):
		""" returns the 2 lists the represent the Masyu board.  ( baseBoard, lineBoard ) """
		return( ( self.baseBoard, self.lineBoard ) )
	def setBoardState( self, stateTuple ):
		""" sets the state of the board to what was saved before.
		@TODO: Make this an internal operation.  No data returned or passed back.
		@TODO: Or, have some sort of checksum to validate the data
		@TODOL Or, encode the state in someway that would make creating the puzzle again difficult.
		"""
		self.baseBoard = stateTuple[0]
		self.lineBoard = stateTuple[1]
	def __str__( self ):
		""" convert the object to a string
		This may look convoluted, and I'm sure it is.
		@TODO: revisit this to make it cleaner.
		@TODO: revisit this to make corners replace empty squares
		@TODO: revisit this to make straight lines replace empty squares
		"""
		# build the base board list of lists
		#  [['.', 'w', 'b'], ['.', '.', '.'], ['b', '.', '.']]
		outBase = [ [ self.baseBoard[y*self.xSize + x] for x in range(self.xSize) ] for y in range(self.ySize) ]
		#print( "outBase: %s" % ( outBase, ) )

		# build the east-west list of lists
		#  [[' ', '-'], [' ', ' '], [' ', ' ']]
		ew = [ [ ((self.lineBoard[y*self.xSize + x] & self.EAST) or (self.lineBoard[y*self.xSize + x + 1] & self.WEST)) and "-" or " " \
				for x in range( self.xSize - 1 ) ] for y in range( self.ySize ) ]
		#print( "ew: %s" % (ew,) )

		# build the north-south list of lists
		#  [[' ', ' ', '|'], [' ', ' ', ' ']]
		ns = [ [ ((self.lineBoard[y*self.xSize + x] & self.SOUTH) or (self.lineBoard[(y+1)*self.xSize + x] & self.NORTH)) and "|" or " " \
				for x in range( self.xSize ) ] for y in range( self.ySize - 1 ) ]
		#print( "ns: %s" % (ns,) )

		# expand the ns list to include spacing spaces
		#  [[' ', ' ', ' ', ' ', '|'], [' ', ' ', ' ', ' ', ' ']]
		ns = map( lambda x: x.split("x"), map( "x x".join, ns ) )
		#print( "ns: %s" % (ns,) )

		# build a zipped list of lists, base board values paired with east-west values
		#  [(['.', 'w', 'b'], [' ', '-']), (['.', '.', '.'], [' ', ' ']), (['b', '.', '.'], [' ', ' '])]
		zipped = zip( outBase, ew )
		#print( "zipped: %s" % ( zipped,) )

		# alternating merge of the values in the tuples.
		#  [['.', ' ', 'w', ' ', 'b'], ['.', ' ', '.', ' ', '.'], ['b', ' ', '.', ' ', '.']]
		mapped = []
		for y in range( self.ySize ):
			row = []
			for x in range( self.xSize ):
				#print( x, y, outBase[y][x] )
				row.append( outBase[y][x] )
				if( x < self.xSize - 1 ):
					row.append( ew[y][x] )
			mapped.append( row )
		#print( "mapped: %s" % ( mapped, ) )

		# merge in the north-south rows
		#  [['.', ' ', 'w', ' ', 'b'], ['  ', '  ', ' '], ['.', ' ', '.', ' ', '.'], ['  ', '  ', ' '], ['b', ' ', '.', ' ', '.']]
		merged = []
		for i in range( len( ns ) ):
			merged.append( mapped[i] )
			merged.append( ns[i] )
		merged.append( mapped[-1] )
		#print( "merged: %s" % (merged,) )

		out = map( "".join, merged )
		return "\n".join( out )