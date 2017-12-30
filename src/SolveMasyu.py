#########################################
# Project:    Masyu Solver
# Filename:   SolveMasyu.py
# Author:     Opussf
# Started:    16 Dec 2017
#########################################
# This drives the solving of a masyu puzzle
#

import MasyuBoard
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
	def solveBoard( self ):
		""" Loop though the functions until the board is solved, or a stalemate is found.
		A board with multiple solutions is possible, an ambigious solution defines an ambigious puzzle.
		I.E. it is the burden of the puzzle to create a single solution.
		if the puzzle has a non-empty square, send it to dot() to determine the color, and call the right function.
		"""
		#print( "=+"*21 )
		for y in range( self.board.ySize ):
			for x in range( self.board.xSize ):
				self.dot( x, y )

	def dot( self, x, y ):
		""" determine the color of the dot, and call the right function """
		square, lines = self.board.getValue( x, y )
		#print( square, lines )
		if square == "b":
			color = self.dotBlack( x, y )
			return color
		elif square == "w":
			color = self.dotWhite( x, y )
			return color
		else:
			return "empty"

	def dotBlack( self, x, y ):
		""" a black dot has to have the line turn 90 degrees.
		the line must go straight for 2 segments in both directions.
		"""
		print( "dotBlack( %i, %i )" % ( x, y ) )
		possibleDirections = 0
		# look for a horizontal line
		# look EAST ( have to be atleast 2 segments from the edge to go EAST )
		if( x < self.board.xSize - 2 ):
			possibleDirections = possibleDirections | self.board.EAST
			print( "Location allows going EAST." )
		# look WEST ( have to be at least 2 segments from the edge to go WEST )
		if( x >= 2 ):
			possibleDirections = possibleDirections | self.board.WEST
			print( "Location allows going WEST." )
		# look for a vertical line
		# look SOUTH
		if( y < self.board.ySize - 2 ):
			possibleDirections = possibleDirections | self.board.SOUTH
			print( "Location allows going SOUTH." )
		# look NORTH
		if( y >= 2 ):
			possibleDirections = possibleDirections | self.board.NORTH
			print( "Location allows going NORTH." )
		print( "possible directions: %5s %5s %5s %5s" % (
			(possibleDirections & self.board.NORTH) and "NORTH" or "",
			(possibleDirections & self.board.EAST) and "EAST" or "",
			(possibleDirections & self.board.SOUTH) and "SOUTH" or "",
			(possibleDirections & self.board.WEST) and "WEST" or "" ))

		if( ( possibleDirections & self.board.NORTH ) and ( possibleDirections & self.board.SOUTH ) ):
			print( "can go both NORTH and SOUTH" )
		elif( possibleDirections & self.board.NORTH ):
			print( "can only go NORTH" )
			self.board.setExit( x, y, self.board.NORTH )
			self.board.setExit( x, y-1, self.board.NORTH )
		elif( possibleDirections & self.board.SOUTH ):
			print( "can only go SOUTH" )
			self.board.setExit( x, y, self.board.SOUTH )
			self.board.setExit( x, y+1, self.board.SOUTH )

		if( ( possibleDirections & self.board.EAST ) and not ( possibleDirections & self.board.WEST ) ):
			print( "can only go EAST" )
			self.board.setExit( x, y, self.board.EAST )
			self.board.setExit( x+1, y, self.board.EAST )
		if( ( possibleDirections & self.board.WEST ) and not ( possibleDirections & self.board.EAST ) ):
			print( "can only go WEST" )
			self.board.setExit( x, y, self.board.WEST )
			self.board.setExit( x-1, y, self.board.WEST )

		print self.board

		return "black"
	def dotWhite( self, x, y ):
		return "white"
