#!/usr/bin/env python
#########################################
# Project:    Masyu Solver
# Filename:   MasyuTXT.py
# Author:     Opussf
# Started:    12 Feb 2017
#########################################
# Allows interaction
#

import MasyuBoard
import SolveMasyu

class MasyuTXT( object ):
	""" User interaction with the Masyu system """

	def __init__( self ):
		self.board = MasyuBoard.MasyuBoard()
		self.X, self.Y = 0, 0
		self.board.initBoard( 3, 3 )
		self.solve = SolveMasyu.SolveMasyu( self.board )
		self.cmds = {
			"x": self.setX,
			"y": self.setY,
			"r": self.restart,
			"l": self.load,
			"q": self.quit,
			"z": self.size,
		}
		self.cmdList = self.cmds.keys()
		self.values = [".","b","w"]
		self.running = True
	def dot( self, color ):
		coordS = raw_input( "\tCoords (x,y)> " )
		coordX, coordY = coordS.split(",")

		self.board.setValue( int(coordX)-1, int(coordY)-1, color )
	def size( self ):
		size = raw_input( "\tNew size (x,y) >" )
		newX, newY = size.split(",")
		self.board.initBoard( int( newX ), int( newY ) )
	def setX( self ):
		X = int( raw_input( "\tSet X > " ) )
		self.X = X - 1
	def setY( self ):
		Y = int( raw_input( "\tSet Y > " ) )
		self.Y = Y - 1
	def restart( self ):
		s = "".join( self.board.baseBoard )
		print s
	def load( self ):
		filename = raw_input( "\tFilename: " )


	def quit( self ):
		self.running=False
	def run( self ):
		while( self.running ):
			self.solve.solveBoard( )
			print( "%s" % ( self.board, ) )
			line = raw_input( "%s Solved: %s%% (%i,%i) >" % ( self.board.boardName, self.board.solvedPercent(), self.X+1, self.Y+1 ) )
			for cmd in line:
				print( "(%i, %i) > %s" % ( self.X+1, self.Y+1, cmd ) )
				if cmd in self.cmdList:
					self.cmds[cmd]()
				if cmd in self.values:
					self.board.setValue( self.X, self.Y, cmd )
					self.X = self.X + 1
					if self.X >= self.board.xSize:
						self.X = 0
						self.Y = self.Y + 1
						if self.Y >= self.board.ySize:
							self.Y = 0





if __name__=="__main__":
	yaya = MasyuTXT()
	yaya.run()
