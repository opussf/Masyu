# Masyu

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

