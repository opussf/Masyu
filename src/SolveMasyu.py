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

	control = {
			MasyuBoard.MasyuBoard.NORTH : { "name": "NORTH", "offsetX":  0, "offsetY": -1 },
			MasyuBoard.MasyuBoard.EAST  : { "name": "EAST",  "offsetX":  1, "offsetY":  0 },
			MasyuBoard.MasyuBoard.SOUTH : { "name": "SOUTH", "offsetX":  0, "offsetY":  1 },
			MasyuBoard.MasyuBoard.WEST  : { "name": "WEST",  "offsetX": -1, "offsetY":  0 },
	}


	def __init__( self, board=None, debug=None ):
		""" create the board else where, init it, populate it, pass it to this object """
		if( board ):
			self.board = board
		else:
			# do something here?
			pass
		self.logger = logging.getLogger( "SolveMasyu" )
		self.logger.setLevel( logging.DEBUG )
		handler = logging.FileHandler( "SolveMasyu.log" )
		handler.setLevel( debug and logging.DEBUG or logging.INFO )
		formatter = logging.Formatter( "%(asctime)s %(levelname)s %(message)s" )
		handler.setFormatter( formatter )
		self.logger.addHandler( handler )
		self.logger.info( "SolveMasyu __init__ completed." )
	def solveBoard( self ):
		""" Loop though the functions until the board is solved, or a stalemate is found.
		A board with multiple solutions is possible, an ambigious solution defines an ambigious puzzle.
		I.E. it is the burden of the puzzle to create a single solution.
		if the puzzle has a non-empty square, send it to dot() to determine the color, and call the right function.
		"""
		self.logger.info( "Starting solveBoard for %s" % ( self.board.filename, ) )
		self.logger.info( "Empty board:\n%s" % ( self.board, ) )
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
						self.logger.info( "%s%%" % ( self.board.solvedPercent(), ) )
					doAgain = result or doAgain
					self.logger.debug( "doAgain: %s" % ( doAgain and "True" or "False", ) )
			self.logger.debug( "End of Loop #%i >>> doAgain: %s" % ( counter, doAgain and "True" or "False" ) )
		self.logger.info( "Final board state of %s:\n%s" % ( self.board.filename, self.board ) )
		self.logger.info( "Solved percent: %s%%" % ( self.board.solvedPercent(), ) )

		if( self.board.filename ):
			fname = self.board.filename.split( "." )
			fname.insert( 1, "solved" )
			fname = ".".join( fname )
			f = open( fname, "w" )
			f.write( "%s\n%s%%" % ( self.board, self.board.solvedPercent() ) )
			f.close()

	def dot( self, x, y ):
		""" determine the color of the dot, and call the right function.
		returns if the function did anything or not """
		dotControl = { "b": self.dotBlack, "w": self.dotWhite, ".": self.dotNone }
		square, lines = self.board.getValue( x, y )
		self.logger.debug( "dot( %i, %i ) square: %s value: %i" % ( x, y, square, lines ) )
		repeatCount = 0
		func = dotControl[square]
		if func:
			self.logger.debug( "a function has been determined for '%s' (%s)." % ( square, func.__name__ ) )
			result = func( x, y )
			while result:
				self.logger.debug( "function made a change, call it again" )
				result = func( x, y )
				repeatCount = repeatCount + 1
			self.logger.debug( "%s( %i, %i ) was repeated %i time%s." % ( func.__name__, x, y, repeatCount, (repeatCount!=1 and "s" or "" ) ) )
			return( repeatCount > 0 )
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

		# self.logger.debug( "impossibleDirections: %s" % ( bin( impossibleDirections ), ) )
		# self.logger.debug( "currentDirections   : %s" % ( bin( currentDirections ), ) )

		# short circut return if good to go
		if currentDirections in [ 3, 6, 12, 9 ]:
			"""
			NE = 3  ( 0011 )
			ES = 6  ( 0110 )
			SW = 12 ( 1100 )
			WN = 9  ( 1001 )
			"""
			# = 0011 ^ 15 = 1100  ^ 0100 = 1000
			requiredNoExits = currentDirections ^ 15 ^ impossibleDirections

			if( requiredNoExits != impossibleDirections ):
				self.logger.debug( "The exits are incomplete." )
				for checkDir in self.control:
					struct = self.control[checkDir]
					self.logger.debug( "Checking %s" % ( struct["name"], ) )
					if( requiredNoExits & checkDir ):
						self.logger.debug( "noExit in %s needs to be set" % ( struct["name"], ) )
						self.board.setNoExit( x, y, checkDir )
						change = True
				self.logger.debug( "this dot has been validated" )
			else:
				self.logger.debug( "this dot is valid, return False" )
			return change

		self.logger.debug( "impossibleDirections: %s" % ( bin( impossibleDirections ), ) )
		self.logger.debug( "currentDirections   : %s" % ( bin( currentDirections ), ) )
		possibleDirections = 0  # use this to set possible directions to choose from

		control = { self.board.NORTH : { "name": "NORTH", "offsetX": 0, "offsetY": -1, "b": self.board.EAST | self.board.WEST, "o": self.board.SOUTH },
				self.board.EAST : { "name": "EAST", "offsetX": 1, "offsetY": 0, "b": self.board.NORTH | self.board.SOUTH, "o": self.board.WEST },
				self.board.SOUTH : { "name": "SOUTH", "offsetX": 0, "offsetY": 1, "b": self.board.EAST | self.board.WEST, "o": self.board.NORTH },
				self.board.WEST : { "name": "WEST", "offsetX": -1, "offsetY": 0, "b": self.board.NORTH | self.board.SOUTH, "o": self.board.EAST }
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
				elif( values & struct["b"] ): # has an exit in the wrong direction
					self.logger.debug( "Neighbor has exit in wrong direction. Cannot go %s. Set noExit" % ( struct["name"], ) )
					self.board.setNoExit( x, y, checkDir )
				else:  # all non directions are eliminated
					possibleDirections = possibleDirections | checkDir  # set this direciton as possible
					self.logger.debug( "Added %s to possibleDirections (%s)" % ( struct["name"], bin( possibleDirections ) ) )
			if( not possibleDirections & checkDir ):  # 0001 & 0001 = 1,
				self.logger.debug( "%s is not possible, setNoExit" % ( struct["name"], ) )
				self.board.setNoExit( x, y, checkDir )

		self.logger.debug( "possible directions: %5s %5s %5s %5s" % (
			(possibleDirections & self.board.WEST) and "WEST" or "",
			(possibleDirections & self.board.SOUTH) and "SOUTH" or "",
			(possibleDirections & self.board.EAST) and "EAST" or "",
			(possibleDirections & self.board.NORTH) and "NORTH" or "" )
			)

		for checkDir in control:
			struct = control[checkDir]
			self.logger.debug( "Processing %s" % ( struct["name"], ) )
			if( ( ( possibleDirections & checkDir ) and not ( possibleDirections & struct["o"] ) ) ):
				self.logger.debug( "Can only go %s" % ( struct["name"], ) )
				if( not currentDirections & checkDir ):
					self.logger.debug( "Not already going %s" % ( struct["name"], ) )
					self.logger.debug( "Marking %s as exit." % ( struct["name"], ) )
					self.board.setExit( x, y, checkDir )
					xPrime = x+struct["offsetX"]
					yPrime = y+struct["offsetY"]
					self.board.setExit( xPrime, yPrime, checkDir )
					for exitDir in control:
						if( struct["b"] & exitDir ):
							self.board.setNoExit( xPrime, yPrime, exitDir )
							self.logger.debug( "Setting noExit( %i, %i, %s )" %
									( xPrime, yPrime, control[exitDir]["name"] ) )
					change = True
			elif( currentDirections & checkDir ):
				self.logger.debug( "already going %s" % ( struct["name"], ) )
				self.board.setNoExit( x, y, struct["o"] )

		#self.logger.info( "\n%s" % ( self.board, ) )
		return change
	def dotWhite( self, x, y ):
		""" a white dot has to have the line go straight through.
		It also has to have the line turn 90 degrees in one of the 2 connected squares.
		1) If a white dot has a noExit on one side (say on the edge) the line has to go 90 degrees to that direction.
		2) If a white dot already has an exit (from another rule) continue through the dot.
		3) If a white dot has another white dot on both sides, those white dots are both blocked directions.
		4) If a white dot has a long line ( next square goes straight ), the opposite direction can be blocked
		5) .-. w w .   Means that the white lines cannot go east - west
		6) .-. w w .-.  Means that the white lines cannot go east - west

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
			NS = 5  ( 0101 )  self.board.NORTH | self.board.SOUTH
			EW = 10 ( 1010 )  self.board.EAST  | self.board.WEST
			"""
			self.logger.debug( "This dot has 2 exits." )
			control = {
					self.board.NORTH : { "name": "NORTH", "offsetX":  0, "offsetY": -1, "o": self.board.SOUTH },
					self.board.EAST  : { "name": "EAST",  "offsetX":  1, "offsetY":  0, "o": self.board.WEST  },
					self.board.SOUTH : { "name": "SOUTH", "offsetX":  0, "offsetY":  1, "o": self.board.NORTH },
					self.board.WEST  : { "name": "WEST",  "offsetX": -1, "offsetY":  0, "o": self.board.EAST  }
			}
			possibleShortDirection = 0
			for checkDir in control:
				struct = control[checkDir]
				if( currentDirections & checkDir ):
					self.logger.debug( "checking %s" % ( struct["name"], ) )
					base, values = self.board.getValue( x+struct["offsetX"], y+struct["offsetY"] )
					if( values & checkDir ):
						self.logger.debug( "neighbor (%i, %i) also exits %s" % ( x+struct["offsetX"], y+struct["offsetY"], struct["name"] ) )
						otherSideX = x+control[struct["o"]]["offsetX"]
						otherSideY = y+control[struct["o"]]["offsetY"]
						self.logger.debug( "validate (%i, %i) terminates" % ( otherSideX, otherSideY ) )
						base, values = self.board.getValue( otherSideX, otherSideY )
						if( self.__oneCount( values & 15 ) == 1 ):  # only look at current exits
							self.logger.debug( "only one entrance" )
							self.logger.debug( "values: %s" % ( bin( values ), ) )
							self.logger.debug( "exit? : %s" % ( bin( struct["o"] << 4 ), ) )

							if( not ( values & ( struct["o"] << 4 ) ) ):
								self.logger.debug( "noExit is not already set" )
								self.board.setNoExit( otherSideX, otherSideY, struct["o"] )
								change = True
			if not change:
				self.logger.debug( "this dot is valid, return False" )
			return change

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
			west = self.board.getValue( x-1, y )
			east = self.board.getValue( x+1, y )
			# check if white dots on both sides
			if( east[0] == "w" and west[0] == "w" ):
				self.logger.debug( "white dots are on both the EAST and the WEST" )
				possibleDirections = ( self.board.NORTH | self.board.SOUTH )
			elif( east[0] == "w" and ( west[1] & 15 == self.board.WEST ) ):
				self.logger.debug( "white dot has a white dot neighbor on the EAST, and an oncoming line on the WEST" )
				possibleDirections = ( self.board.NORTH | self.board.SOUTH )
			elif( west[0] == "w" and ( east[1] & 15 == self.board.EAST ) ):
				self.logger.debug( "white dot has a white dot neighbor on the WEST, and an oncoming line on the EAST" )
				possibleDirections = ( self.board.NORTH | self.board.SOUTH )
			elif( ( east[1] & 15 == self.board.EAST ) and ( west[1] & 15 == self.board.WEST ) ):
				self.logger.debug( "white dot has 2 incoming lines EAST and WEST, set NORTH and SOUTH directions" )
				possibleDirections = ( self.board.NORTH | self.board.SOUTH )
		except ValueError:  # a ValueError is expected if on the east or west edge
			pass
		try:
			north = self.board.getValue( x, y-1 )
			south = self.board.getValue( x, y+1 )
			if( north[0] == "w" and south[0] == "w" ):
				self.logger.debug( "white dots are on both the NORTH and the SOUTH" )
				possibleDirections = ( self.board.EAST | self.board.WEST )
			elif( north[0] == "w" and ( south[1] & 15 == self.board.SOUTH ) ):
				self.logger.debug( "white dot has a white dot neighbor on the NORTH, and an oncoming line on the SOUTH" )
				possibleDirections = ( self.board.EAST | self.board.WEST )
			elif( south[0] == "w" and ( north[1] & 15 == self.board.NORTH ) ):
				self.logger.debug( "white dot has a white dot neighbor on the SOUTH, and an oncoming line on the NORTH" )
				possibleDirections = ( self.board.EAST | self.board.WEST )
			elif( ( north[1] & 15 == self.board.NORTH ) and ( south[1] & 15 == self.board.SOUTH ) ):
				self.logger.debug( "white dot has 2 incoming lines NORTH and SOUTH, set EAST and WEST directions" )
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

	def followLine( self, x, y, direction=None ):
		""" direction is the direction you came from (ignore it)
		"""
		control = {
				self.board.NORTH : { "name": "NORTH", "offsetX":  0, "offsetY": -1, "o": self.board.SOUTH },
				self.board.EAST  : { "name": "EAST",  "offsetX":  1, "offsetY":  0, "o": self.board.WEST  },
				self.board.SOUTH : { "name": "SOUTH", "offsetX":  0, "offsetY":  1, "o": self.board.NORTH },
				self.board.WEST  : { "name": "WEST",  "offsetX": -1, "offsetY":  0, "o": self.board.EAST  }
		}
		self.logger.debug( "Entering followLine( %i, %i, %s )" % ( x, y, (direction and control[direction]["name"] or "None" ) ) )
		exitValues = self.board.getValue( x, y )[1]
		currentDirections = exitValues & 15
		self.logger.debug( "exitValues: %s currentDirections: %s" % ( bin( exitValues ), bin( currentDirections ) ) )
		currentDirectionCount = self.__oneCount( currentDirections )
		if( currentDirectionCount == 1 and direction ):
			self.logger.debug( "Found the end of the line at ( %i, %i )" % ( x, y ) )
			return( ( x, y ) )
		else:
			self.logger.debug( "currentDirections: %s direction: %s" % ( bin( currentDirections ), ( direction or "None" ) ) )
			goDir = currentDirections ^ (direction or 0)
			self.logger.debug( "goDir: %s" % ( bin( goDir ), ) )
			self.logger.debug( "Follow the line to the %s" % ( control[goDir]["name"], ) )
			return( self.followLine( x+control[goDir]["offsetX"], y+control[goDir]["offsetY"], control[goDir]["o"] ) )

	def dotNone( self, x, y ):
		""" 'empty' dots follow a few rules as well.
		1) if a line enters it, with only one exit, use that exit.
		2) if there are 3 noExits, set the 4th noExit. ( no way to exit if entered )
		3) if there are 2 used exits, make sure that the other directions are marked as noExit
		4) if a line enters it, follow the line.
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
		# 4) single line, follow the line
		if( currentDirectionCount == 1 ):
			if( impossibleDirectionCount == 2 ):
				self.logger.debug( "dot has a line, and a single exit available." )
				self.board.setExit( x, y, missingDirections )
				change = True
			elif( impossibleDirectionCount < 2 ):
				endX, endY = self.followLine( x, y )
				self.logger.debug( "Line starting at ( %i, %i ) ends at ( %i, %i )" % ( x, y, endX, endY ) )
				distance = abs( endX - x ) + abs( endY - y )
				if( distance == 1 ):
					if( x == endX ):
						if( endY > y and ( not impossibleDirections & self.board.SOUTH ) ):
							self.logger.debug( "no south" )
							self.board.setNoExit( x, y, self.board.SOUTH )
							change = True
						if( endY < y and ( not impossibleDirections & self.board.NORTH ) ):
							self.logger.debug( "no north" )
							self.board.setNoExit( x, y, self.board.NORTH )
							change = True
					if( y == endY ):
						if( endX > x and ( not impossibleDirections & self.board.EAST ) ):
							self.logger.debug( "no east" )
							self.board.setNoExit( x, y, self.board.EAST )
							change = True
						if( endX < x and ( not impossibleDirections & self.board.WEST ) ):
							self.logger.debug( "no west" )
							self.board.setNoExit( x, y, self.board.WEST )
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
				self.logger.debug( "2 lines, set NORTH noexit" )
				self.board.setNoExit( x, y, self.board.NORTH )
			if( missingDirections & self.board.EAST ):
				self.logger.debug( "2 lines, set EAST noexit" )
				self.board.setNoExit( x, y, self.board.EAST )
			if( missingDirections & self.board.SOUTH ):
				self.logger.debug( "2 lines, set SOUTH noexit" )
				self.board.setNoExit( x, y, self.board.SOUTH )
			if( missingDirections & self.board.WEST ):
				self.logger.debug( "2 lines, set WEST noexit" )
				self.board.setNoExit( x, y, self.board.WEST )
			self.board.setNoExit( x, y, missingDirections )
			change = True

		return change
