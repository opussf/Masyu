# Masyu

[![Build Status](https://travis-ci.org/opussf/Masyu.svg?branch=master)](https://travis-ci.org/opussf/Masyu)

Masyu is a puzzle game where dots in a grid provide hints to connect all the dots with a single closed loop.

## Start

A grid has black / solid circles, and white / hollow circles.
The different circles have different rules:

* Solid circles
	* The line must turn 90 degrees, or they need to be a corner.
	* The line must be at least 2 units long on both sides.

	┌─┬─┬─┐
	│────●│
	├─┼─┼│┤
	│ │ │││
	├─┼─┼│┤
	│ │ │││
	└─┴─┴─┘

* Hollow circles
	* The line must go straight through.
	* The line must turn in the previous and/or next cell.

	┌─┬─┬─┐
	│ │ │┐│
	├─┼─┼│┤
	│ │ │○│
	├─┼─┼│┤
	│ │ │┘│
	└─┴─┴─┘

## Printed board

		. w─b
		    │
		. . .

		b . .

─ = \u2500
│ = \u2502
┌ = \u250c
┐ = \u2510
└ = \u2514
┘ = \u2518
http://jrgraphix.net/r/Unicode/2500-257F

## Ideas

Create a board object that holds, as 2 data structures, both the original board and the line.
The line is stored as known exit points from that square, and known non-exit points.





* Solid circle
	* 90 degree turn
	* line goes 2 segments in one direction
		* if line cannot go two, then block that direction
		* block the sides of the line drawn
	* if exit direction is blocked, go opposite direction
	* if a 2 segment line would enter a segment with a pre-existing exit in the first segment, block that direction.


* While circle
	* stright line
		* if a direction is blocked, draw the line, block the other direction.
	* scan up to 3 blocks in each direction
		* if 3 white circles in that direction, block it.
	* if a line exists to it, draw the other exit.
	* if one of the lines goes longer than 1 segment, block the end of the other direction
	* if there is a white circle on two opposite sides, do not go into them


* Line escape
	* if only one exit is possible, use it.
	* if drawing a line in a direction causes a closed loop that does not solve the puzzle, block it
