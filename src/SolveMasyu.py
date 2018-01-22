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
					doAgain = self.dot( x, y ) or doAgain
					self.logger.debug( "doAgain: %s" % ( doAgain and "True" or "False", ) )
			self.logger.debug( "End of Loop  >>> doAgain: %s" % ( doAgain and "True" or "False", ) )

	def dot( self, x, y ):
		""" determine the color of the dot, and call the right function.
		returns if the function did anything or not """
		square, lines = self.board.getValue( x, y )
		self.logger.debug( "dot( %i, %i ) square: %s value: %i" % ( x, y, square, lines ) )
		if square == "b":
			return self.dotBlack( x, y )
		elif square == "w":
			color = self.dotWhite( x, y )
			#self.logger.debug( "color: %s" % ( color, ) )
			return color
		else:
			self.logger.debug( "empty" )
			return False

	def dotBlack( self, x, y ):
		""" a black dot has to have the line turn 90 degrees.
		the line must go straight for 2 segments in both directions.

		WSEN
		8421
		"""
		self.logger.debug( "dotBlack( %i, %i )" % ( x, y ) )
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
		if( not impossibleDirections & self.board.NORTH ):  # north is possible
			self.logger.debug( "north is possible: 1" )
			base, values = self.board.getValue( x, y-1 )
			if( ( not values >> 4 & self.board.NORTH ) and ( not base == "b" ) ):
				self.logger.debug( "north is possible: 2" )
				possibleDirections = possibleDirections | self.board.NORTH
		if( not possibleDirections & self.board.NORTH ):
			self.logger.debug( "north is not possible. setNoExit" )
			self.board.setNoExit( x, y, self.board.NORTH )
		# look EAST
		if( not impossibleDirections & self.board.EAST ):  # east is possible
			self.logger.debug( "east is possible: 1" )
			base, values = self.board.getValue( x+1, y )
			if( ( not values >> 4 & self.board.EAST ) and ( not base == "b" ) ):
				self.logger.debug( "east is possible: 2" )
				possibleDirections = possibleDirections | self.board.EAST
		if( not possibleDirections & self.board.EAST ):
			self.logger.debug( "east is not possible. setNoExit" )
			self.board.setNoExit( x, y, self.board.EAST )
		# look SOUTH
		if( not impossibleDirections & self.board.SOUTH ):  # south is possible
			self.logger.debug( "south is possible: 1" )
			if( not self.board.getValue( x, y+1 )[1] >> 4 & self.board.SOUTH ):
				self.logger.debug( "south is possible: 2" )
				possibleDirections = possibleDirections | self.board.SOUTH
		if( not possibleDirections & self.board.SOUTH ):
			self.logger.debug( "south is not possible. setNoExit" )
			self.board.setNoExit( x, y, self.board.SOUTH )
		# look WEST
		if( not impossibleDirections & self.board.WEST ):  # west is possible
			self.logger.debug( "west is possible: 1" )
			if( not self.board.getValue( x-1, y )[1] >> 4 & self.board.WEST ):
				self.logger.debug( "west is possible: 2" )
				possibleDirections = possibleDirections | self.board.WEST
		if( not possibleDirections & self.board.WEST ):
			self.logger.debug( "west is not possible. setNoExit" )
			self.board.setNoExit( x, y, self.board.WEST )

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
				self.board.setNoExit( x, y-1, self.board.EAST | self.board.WEST )
				change = True
		if( ( possibleDirections & self.board.SOUTH ) and not ( possibleDirections & self.board.NORTH ) ):
			self.logger.debug( "can only go SOUTH" )
			if( not currentDirections & self.board.SOUTH ):
				self.logger.debug( "not already going SOUTH" )
				self.board.setExit( x, y, self.board.SOUTH )
				self.board.setExit( x, y+1, self.board.SOUTH )
				self.board.setNoExit( x, y+1, self.board.EAST | self.board.WEST )
				change = True

		if( ( possibleDirections & self.board.EAST ) and not ( possibleDirections & self.board.WEST ) ):
			self.logger.debug( "can only go EAST" )
			if( not currentDirections & self.board.EAST ):
				self.logger.debug( "not already going EAST" )
				self.board.setExit( x, y, self.board.EAST )
				self.board.setExit( x+1, y, self.board.EAST )
				self.board.setNoExit( x+1, y, self.board.NORTH | self.board.SOUTH )
				change = True
		if( ( possibleDirections & self.board.WEST ) and not ( possibleDirections & self.board.EAST ) ):
			self.logger.debug( "can only go WEST" )
			if( not currentDirections & self.board.WEST ):
				self.logger.debug( "not already going WEST" )
				self.board.setExit( x, y, self.board.WEST )
				self.board.setExit( x-1, y, self.board.WEST )
				self.board.setNoExit( x-1, y, self.board.NORTH | self.board.SOUTH )
				change = True

		self.logger.debug( "\n%s" % self.board )

		return change
	def dotWhite( self, x, y ):
		""" a white dot has to have the line go straight through.
		It also has to have the line turn 90 degrees in one of the 2 connected squares.

		WSEN
		8421
		"""
		self.logger.debug( "dotWhite( %i, %i )" % ( x, y ) )
		change = False

		exitValues = self.board.getValue( x, y )[1]
		impossibleDirections = exitValues >> 4
		currentDirections = exitValues & 15

		self.logger.debug( "impossibleDirections: %s" % ( bin( impossibleDirections ), ) )
		self.logger.debug( "currentDirections   : %s" % ( bin( currentDirections ), ) )


		return change
