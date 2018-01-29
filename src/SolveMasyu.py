#########################################
# Project:    Masyu Solver
# Filename:   SolveMasyu.py
# Author:     Opussf
# Started:    16 Dec 2017
#########################################
# This drives the solving of a masyu puzzle
#

import MasyuBoard
import logging
#import time

class SolveMasyu( object ):
	""" solve a MasyuBoard.
	While puzzles may present multiple solutions, this tries to find the 'optimal' ones.
	An 'optimal' solution is defined as having the shortest line that go through all given dots, with the least number of corners.
	A 3x3 puzzle with a single black dot in a corner will solve as a square (4 corners).
	Any single black dot puzzle solves to a 3x3 square (line goes 2 lengths).
	A single white dot puzzle solves to a 3x2 rectangle (has to turn previous and/or next square).
	"""
	def __init__( self, board=None ):
		""" create the board else where, init it, populate it, pass it to this object """
		if( board ):
			self.board = board
		else:
			# do something here?
			pass
		self.logger = logging.getLogger( "SolveMasyu" )
		self.logger.setLevel( logging.DEBUG )
		handler = logging.FileHandler( "SolveMasyu.log" )
		handler.setLevel( logging.DEBUG )
		formatter = logging.Formatter( "%(asctime)s %(levelname)s %(message)s" )
		handler.setFormatter( formatter )
		self.logger.addHandler( handler )
		self.logger.info( "SolveMasyu __init__ completed." )
	def __del__( self ):
		self.logger.info( "Shutting down" )
		self.logger.shutdown()
	def solveBoard( self ):
		""" Loop though the functions until the board is solved, or a stalemate is found.
		A board with multiple solutions is possible, an ambigious solution defines an ambigious puzzle.
		I.E. it is the burden of the puzzle to create a single solution.
		if the puzzle has a non-empty square, send it to dot() to determine the color, and call the right function.
		"""
		self.logger.debug( "Starting solveBoard" )
		doAgain = True
		counter = 0
		while doAgain:
			counter += 1
			self.logger.debug( "loop #%i" % ( counter, ) )
			doAgain = False
			for y in range( self.board.ySize ):
				for x in range( self.board.xSize ):
					result = self.dot( x, y )
					if( result ):
						self.logger.info( "\n%s" % ( self.board, ) )
					doAgain = result or doAgain
					self.logger.debug( "doAgain: %s" % ( doAgain and "True" or "False", ) )
			self.logger.debug( "End of Loop  >>> doAgain: %s" % ( doAgain and "True" or "False", ) )
		self.logger.info( "Final board state:\n%s" % ( self.board, ) )

	def dot( self, x, y ):
		""" determine the color of the dot, and call the right function.
		returns if the function did anything or not """
		square, lines = self.board.getValue( x, y )
		self.logger.debug( "dot( %i, %i ) square: %s value: %i" % ( x, y, square, lines ) )
		if square == "b":
			return self.dotBlack( x, y )
		elif square == "w":
			return self.dotWhite( x, y )
		elif square == ".":
			return self.dotNone( x, y )
		else: # maybe this should be an error?
			return False

	def dotBlack( self, x, y ):
		""" a black dot has to have the line turn 90 degrees.
		the line must go straight for 2 segments in both directions.

		WSEN
		8421
		"""
		self.logger.debug( "dotBlack( %i, %i )" % ( x, y ) )
		self.logger.info( "\n%s" % ( self.board, ) )
		change = False

		exitValues = self.board.getValue( x, y )[1]
		impossibleDirections = exitValues >> 4
		currentDirections = exitValues & 15

		self.logger.debug( "impossibleDirections: %s" % ( bin( impossibleDirections ), ) )
		self.logger.debug( "currentDirections   : %s" % ( bin( currentDirections ), ) )


		if currentDirections in [ 3, 6, 12, 9 ]:
			"""
			NE = 3  ( 0011 )
			ES = 6  ( 0110 )
			SW = 12 ( 1100 )
			WN = 9  ( 1001 )
			"""
			self.logger.debug( "this dot is valid, return False" )
			return False

		possibleDirections = 0  # use this to set possible directions to choose from
		# look for a horizontal line
		# look NORTH ( have at least 2 segments to travel )

		control = { self.board.NORTH : { "name": "NORTH", "offsetX": 0, "offsetY": -1, "b": self.board.EAST | self.board.WEST },
				self.board.EAST : { "name": "EAST", "offsetX": 1, "offsetY": 0, "b": self.board.NORTH | self.board.SOUTH },
				self.board.SOUTH : { "name": "SOUTH", "offsetX": 0, "offsetY": 1, "b": self.board.EAST | self.board.WEST },
				self.board.WEST : { "name": "WEST", "offsetX": -1, "offsetY": 0, "b": self.board.NORTH | self.board.SOUTH }
				}

		for checkDir in control:
			struct = control[checkDir]
			self.logger.debug( "Checking %s (%s)" % ( struct["name"], bin( checkDir ) ) )
			if( not impossibleDirections & checkDir ):  # this direction is possible
				self.logger.debug( "%s is possible: 1" % ( struct["name"], ) )
				base, values = self.board.getValue( x+struct["offsetX"], y+struct["offsetY"] )
				self.logger.debug( "check neighbor" )
				self.logger.debug( "values(%s) & 'b'(%s): %s" % ( bin( values ), bin( struct["b"] ), bin( values & struct["b"] ) ) )
				if( base == "b" ):  # cannot go through a neighbor black dot
					self.logger.debug( "Found another black dot to the %s. Set noExit" % ( struct["name"], ) )
					self.board.setNoExit( x, y, checkDir )
				elif( ( values >> 4 & checkDir ) ):  # neighbor cannot exit in the direction we need to go
					# 1000 & 1000 = 1000  (true) 0000 & 1000 = 0 (false)
					self.logger.debug( "Cannot exit to the %s. Set noExit" % ( struct["name"], ) )
					self.board.setNoExit( x, y, checkDir )

				else:  # all non directions are eliminated
					possibleDirections = possibleDirections | checkDir  # set this direciton as possible
					self.logger.debug( "Added %s to possibleDirections (%s)" % ( struct["name"], bin( possibleDirections ) ) )
			if( not possibleDirections & checkDir ):  # 0001 & 0001 = 1,
				self.logger.debug( "%s is not possible, setNoExit" % ( struct["name"], ) )
				self.board.setNoExit( x, y, checkDir )

		self.logger.debug( "possible directions: %5s %5s %5s %5s" % (
			(possibleDirections & self.board.NORTH) and "NORTH" or "",
			(possibleDirections & self.board.EAST) and "EAST" or "",
			(possibleDirections & self.board.SOUTH) and "SOUTH" or "",
			(possibleDirections & self.board.WEST) and "WEST" or "" ))

		if( ( possibleDirections & self.board.NORTH ) and not ( possibleDirections & self.board.SOUTH ) ):
			self.logger.debug( "can only go NORTH" )
			if( not currentDirections & self.board.NORTH ):
				self.logger.debug( "not already going NORTH")
				self.board.setExit( x, y, self.board.NORTH )
				self.board.setExit( x, y-1, self.board.NORTH )
				self.board.setNoExit( x, y-1, self.board.EAST )
				self.board.setNoExit( x, y-1, self.board.WEST )
				change = True
		if( ( possibleDirections & self.board.SOUTH ) and not ( possibleDirections & self.board.NORTH ) ):
			self.logger.debug( "can only go SOUTH" )
			if( not currentDirections & self.board.SOUTH ):
				self.logger.debug( "not already going SOUTH" )
				self.board.setExit( x, y, self.board.SOUTH )
				self.board.setExit( x, y+1, self.board.SOUTH )
				self.board.setNoExit( x, y+1, self.board.EAST )
				self.board.setNoExit( x, y+1, self.board.WEST )
				change = True

		if( ( possibleDirections & self.board.EAST ) and not ( possibleDirections & self.board.WEST ) ):
			self.logger.debug( "can only go EAST" )
			if( not currentDirections & self.board.EAST ):
				self.logger.debug( "not already going EAST" )
				self.board.setExit( x, y, self.board.EAST )
				self.board.setExit( x+1, y, self.board.EAST )
				self.board.setNoExit( x+1, y, self.board.NORTH )
				self.board.setNoExit( x+1, y, self.board.SOUTH )
				change = True
		if( ( possibleDirections & self.board.WEST ) and not ( possibleDirections & self.board.EAST ) ):
			self.logger.debug( "can only go WEST" )
			if( not currentDirections & self.board.WEST ):
				self.logger.debug( "not already going WEST" )
				self.board.setExit( x, y, self.board.WEST )
				self.board.setExit( x-1, y, self.board.WEST )
				self.board.setNoExit( x-1, y, self.board.NORTH )
				self.board.setNoExit( x-1, y, self.board.SOUTH )
				change = True

		#self.logger.debug( "\n%s" % self.board )

		return change
	def dotWhite( self, x, y ):
		""" a white dot has to have the line go straight through.
		It also has to have the line turn 90 degrees in one of the 2 connected squares.
		1) If a white dot has a noExit on one side (say on the edge) the line has to go 90 degrees to that direction.
		2) If a white dot already has an exit (from another rule) continue through the dot.
		3) If a white dot has another white dot on both sides, those white dots are both blocked directions.
		4) If a white dot has a long line ( next square goes straight ), the opposite direction can be blocked

		WSEN
		8421
		"""
		self.logger.debug( "dotWhite( %i, %i )" % ( x, y ) )
		change = False

		exitValues = self.board.getValue( x, y )[1]
		impossibleDirections = exitValues >> 4
		currentDirections = exitValues & 15

		if currentDirections in [ 5, 10 ]:
			"""
			NS = 5  ( 0101 )
			EW = 10 ( 1010 )
			"""
			self.logger.debug( "this dot is valid, return False" )
			return False

		possibleDirections = 0
		self.logger.debug( "impossibleDirections: %s" % ( bin( impossibleDirections ), ) )
		self.logger.debug( "currentDirections   : %s" % ( bin( currentDirections ), ) )

		# look for impossible directions
		if( impossibleDirections & self.board.NORTH ):
			self.logger.debug( "cannot go NORTH" )
			possibleDirections = ( self.board.EAST | self.board.WEST )
		if( impossibleDirections & self.board.EAST ):
			self.logger.debug( "cannot go EAST" )
			possibleDirections = ( self.board.NORTH | self.board.SOUTH )
		if( impossibleDirections & self.board.SOUTH ):
			self.logger.debug( "cannot go SOUTH" )
			possibleDirections = ( self.board.EAST | self.board.WEST )
		if( impossibleDirections & self.board.WEST ):
			self.logger.debug( "cannot go WEST" )
			possibleDirections = ( self.board.NORTH | self.board.SOUTH )

		# look for partial directions
		if( ( currentDirections & self.board.NORTH ) or ( currentDirections & self.board.SOUTH ) ): # north or south are already given
			self.logger.debug( "found a current line going NORTH or SOUTH" )
			possibleDirections = ( self.board.NORTH | self.board.SOUTH )
		if( ( currentDirections & self.board.EAST ) or ( currentDirections & self.board.WEST ) ): # east or west are already given
			self.logger.debug( "found a current line going EAST or WEST" )
			possibleDirections = ( self.board.EAST | self.board.WEST )

		# look for two other whitedots
		try:
			westVal = self.board.getValue( x-1, y )[0]
			eastVal = self.board.getValue( x+1, y )[0]
			if( westVal == "w" and eastVal == "w" ):
				self.logger.debug( "white dots are on both the EAST and the WEST" )
				possibleDirections = ( self.board.NORTH | self.board.SOUTH )
		except ValueError:  # a ValueError is expected if on the east or west edge
			pass
		try:
			northVal = self.board.getValue( x, y-1 )[0]
			southVal = self.board.getValue( x, y+1 )[0]
			if( northVal == "w" and southVal == "w" ):
				self.logger.debug( "white dots are on both the NORTH and the SOUTH" )
				possibleDirections = ( self.board.EAST | self.board.WEST )
		except ValueError:  # a ValueError is expected if on the north or south edge
			pass

		# process possibleDirections
		if( possibleDirections != 0 ):
			self.logger.debug( "possibleDirections is not 0 (%s)" % (bin( possibleDirections ), ) )
			if( possibleDirections == self.board.EAST | self.board.WEST ):
				self.logger.debug( "drawing line EAST and WEST" )
				self.board.setExit( x, y, self.board.EAST )
				self.board.setExit( x, y, self.board.WEST )
				self.logger.debug( "blocking the other directions" )
				self.board.setNoExit( x, y, self.board.NORTH )
				self.board.setNoExit( x, y, self.board.SOUTH )
				change = True
			if( possibleDirections == self.board.NORTH | self.board.SOUTH ):
				self.logger.debug( "drawing line NORTH and SOUTH" )
				self.board.setExit( x, y, self.board.NORTH )
				self.board.setExit( x, y, self.board.SOUTH )
				self.logger.debug( "blocking the other directions" )
				self.board.setNoExit( x, y, self.board.EAST )
				self.board.setNoExit( x, y, self.board.WEST )
				change = True


		#self.logger.debug( "\n%s" % self.board )

		return change

	def __oneCount( self, val ):
		count = 0
		while val > 0:
			if val & 1:
				count += 1
			val = val >> 1
		return count

	def dotNone( self, x, y ):
		""" 'empty' dots follow a few rules as well.
		1) if a line enters it, with only one exit, use that exit.
		2) if there are 3 noExits, set the 4th noExit. ( no way to exit if entered )
		3) if there are 2 used exits, make sure that the other directions are marked as noExit
		"""
		self.logger.debug( "dotNone( %i, %i )" % ( x, y ) )
		change = False

		exitValues = self.board.getValue( x, y )[1]
		impossibleDirections = exitValues >> 4
		currentDirections = exitValues & 15

		self.logger.debug( "impossibleDirections: %s" % ( bin( impossibleDirections ), ) )
		self.logger.debug( "currentDirections   : %s" % ( bin( currentDirections ), ) )
		missingDirections = 15 - ( impossibleDirections ^ currentDirections )  # directions not used.
		""" 0101 ^ 1000 = 1101    1101 ^ 1111 = 0010
		"""

		currentDirectionCount = self.__oneCount( currentDirections )
		impossibleDirectionCount = self.__oneCount( impossibleDirections )

		self.logger.debug( "currentDirectionCount   : %i" % ( currentDirectionCount, ) )
		self.logger.debug( "impossibleDirectionCount: %i" % ( impossibleDirectionCount, ) )
		self.logger.debug( "missingDirections   : %s" % ( bin( missingDirections ), ) )

		# 1) single line, 2 impossible exits
		if( currentDirectionCount == 1 and impossibleDirectionCount == 2 ):
			self.logger.debug( "dot has a line, and a single exit available." )
			self.board.setExit( x, y, missingDirections )
			change = True
		# 2) 3 noExits
		if( impossibleDirectionCount == 3 ):
			self.logger.debug( "dot has 3 noExits" )
			self.board.setNoExit( x, y, missingDirections )
			change = True
		# 3)
		if( currentDirectionCount == 2 and impossibleDirectionCount != 2 ):
			self.logger.debug( "dot has 2 lines, need to set the final exit." )
			if( missingDirections & self.board.NORTH ):
				self.logger.debug( "2 lines, set NORTH exit" )
				self.board.setNoExit( x, y, self.board.NORTH )
			if( missingDirections & self.board.EAST ):
				self.logger.debug( "2 lines, set EAST exit" )
				self.board.setNoExit( x, y, self.board.EAST )
			if( missingDirections & self.board.SOUTH ):
				self.logger.debug( "2 lines, set SOUTH exit" )
				self.board.setNoExit( x, y, self.board.SOUTH )
			if( missingDirections & self.board.WEST ):
				self.logger.debug( "2 lines, set WEST exit" )
				self.board.setNoExit( x, y, self.board.WEST )
			self.board.setNoExit( x, y, missingDirections )
			change = True

		return change
