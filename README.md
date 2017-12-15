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

