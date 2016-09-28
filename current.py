#!usr/bin/env python

import random, os, csp_solver_4
num_chords = 128

chords = [ 1 ] 
current_chord = []

note_names = [ None, "a,,,", "ais,,,", "b,,,", "c,,", "cis,,", "d,,", "dis,,", "e,,", "f,,", "fis,,", "g,,", "gis,,", "a,,", "ais,,", "b,,", "c,", "cis,", "d,", "dis,", "e,", "f,", "fis,", "g,", "gis,", "a,", "ais,", "b,", "c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b", "c'", "cis'", "d'", "dis'", "e'", "f'", "fis'", "g'", "gis'", "a'", "ais'", "b'", "c''", "cis''", "d''", "dis''", "e''", "f''", "fis''", "g''", "gis''", "a''", "ais''", "b''", "c''',", "cis'''", "d'''", "dis'''", "e'''", "f'''", "fis'''", "g'''", "gis'''", "a'''", "ais'''", "b'''", "c''''", "cis''''", "d''''", "dis''''", "e''''", "f''''", "fis''''", "g''''", "gis''''", "a''''", "ais''''", "b''''", "c'''''" ]

def constraint_func( A, a, B, b ):
	global current_chord
	if (a<b and A>B) or (a>b and A<B) or a==b:
		return False
	if abs(A-B)==1 and ( abs(a-b)>12 ):
		return False
	if A!=0 and B!=0 and ( abs(current_chord[A]-current_chord[B])==24 and abs(a-b)==24 ):
		return False
	if A!=0 and B!=0 and ( abs(current_chord[A]-current_chord[B])==12 and abs(a-b)==12 ):
		return False
	if ( abs(current_chord[A]-current_chord[B])==7 and abs(a-b)==7 ):
		return False
	return True

def findPossibles( degree ):
	if degree == 1: return [ 4, 8, 11 ]
	elif degree == 2: return [ 1, 6, 9 ]
	elif degree == 3: return [ 3, 8, 11 ]
	elif degree == 4: return [ 1, 4, 9 ]
	elif degree == 5: return [ 3, 6, 11 ]
	elif degree == 6: return [ 1, 4, 8 ]
	elif degree == 7: return [ 3, 6, 9 ]
	
def limit_domains( domains ):
	for x in domains[0]:
		if x<20:
			domains[0].remove( x )
	for x in domains[1]:
		if x<28:
			domains[1].remove( x )
	for x in domains[2]:
		if x<36:
			domains[2].remove( x )
	for x in domains[3]:
		if x<44:
			domains[3].remove( x )
	return domains

def readin( filename ):
	file = open( filename, "r" )
	temp = file.read().split('\n')[:-1]

	progressions = {}
	for i in temp:
		item = i.split( ',' )
		
		item2 = []
		for j in item:
			item2.append( int( j ) )
		progressions[ item2[0] ] = item2[1:]
	return progressions
prog_back = readin( "prog_backward.csv" )
prog_forw = readin( "prog_forward.csv" )

def step( progressions, curchord ):
	neighbors = progressions[ curchord ]
	return neighbors[ random.randint( 0, len( neighbors )-1 ) ]

def write( current, next, index ):
	global current_chord, chords
	current_chord = current
	
	possible = findPossibles( next )
	options = []
	
	min, max = current[0], current[3]
	for opt in possible:
		for x in range( 1, 6 ):
			val = opt+x*12
			if val > 59:
				continue;
			if val>min and val<max:
				if val not in options:
					options.append( val )
			elif abs( val-min ) < 8:
				if val not in options:
					options.append( val )
			elif abs( val-max ) < 8:
				if val not in options:
					options.append( val )
#	print "%i:" % (next),
#	print options
#	print current_chord

	domains = {}
	for x in xrange( len( current ) ):
		domain = []
		for y in options:
			if abs( current[x]-y ) < 4:
				domain.append( y )
		domains[ x ] = domain
	domains = limit_domains( domains )

	grid, constraints = {}, {}
	for x in xrange( 4 ):
		grid[ x ] = []
		for y in xrange( 4 ):
			if x!=y:
				grid[ x ].append( y )
	for node in grid:
		constraints[ node ] = []
		for neighbor in grid[ node ]:
			constraints[ node ].append( [ neighbor, constraint_func ] )

	assignments = {}
	if csp_solver_4.backtracking( domains, assignments, constraints ):
		retval = []	
		for x in xrange( len( assignments ) ):
			retval.append( assignments[x] )
		return retval
	else:
#		next = step( prog_forw, chords[index] )
		return write( [28,35,40,44], next, index )

for x in xrange( num_chords-1 ):
	chords.append( step( prog_back, chords[x] ) )
chords.append( 1 )
chords.reverse()
#print chords

parts = [ [28,35,40,44] ]
for x in xrange( len( chords )-1 ):
	parts.append( write( parts[x], chords[x+1], x ) )
#print parts

fh = open( "output_numbers.txt", "w" )
for x in xrange( len( parts ) ):
	for y in xrange( len( parts[x] )-1 ):
		fh.write( "%s," % ( parts[x][y] ) )
	fh.write( "%s\n" % ( parts[x][ len( parts[x] )-1 ] ) )
fh.close()

os.system( "python parse.py" )
