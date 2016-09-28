def backtracking( domains, assignments, constraints ):
	if len( assignments ) == len( domains ):
		return True

	next_var = find_min( domains, assignments, constraints )
	unique_list = []
	def sort_func( a, b ): # --- LEAST CONSTRAINING VALUE FUNCTION --- #
		counter_a = 0
		counter_b = 0
		for constraint_pair in constraints[ next_var ]:
			nbr, constraint = constraint_pair
			if nbr in assignments:
				continue
			if nbr in unique_list:
				continue
			else:
				unique_list.append( nbr )

			for possible in domains[ nbr ]:
				if not constraint( next_var, a, nbr, possible  ):
					counter_a += 1

			for possible in domains[ nbr ]:
				if not constraint( next_var, b, nbr, possible ):
					counter_b += 1
		return counter_a - counter_b
	domains[ next_var ].sort( sort_func )

#	print domains[ next_var ]
	for possible_val in domains[ next_var ]:
		for constraint_pair in constraints[ next_var ]:
			nbr, constraint = constraint_pair
			
			if nbr not in assignments:
				continue
			
			if not constraint( next_var, possible_val, nbr, assignments[ nbr ] ):
				break
		else:
#			print "Assigning [%s]: %s" % (next_var, possible_val)
			assignments[ next_var ] = possible_val
			
			new_domains = {}
			for i in domains.keys():
				new_domains[i] = domains[i][:]

			for constraint_pair in constraints[ next_var ]:
				counter = 0
				nbr, constraint = constraint_pair	

				for possible in domains[ nbr ]:
					if possible in new_domains[ nbr ]:
						if not constraint( next_var, possible_val, nbr, possible ):
#							print "Removing %s from %s" % ( possible, nbr )
							new_domains[ nbr ].remove( possible )
			if backtracking( new_domains, assignments, constraints ):
				return True
			else:
				del assignments[ next_var ]
	print "Backtracking..."
	return False

def find_min( domains, assignments, constraints ):
	def sort_func( a, b ): # --- SORT BY AMOUNT OF POSSIBLE VALUES --- #
		return len( domains[ a ] ) - len( domains[ b ] )
	
	def sort_func2( a, b ): # --- SORT BY AMOUNT OF UNASSIGNED NEIGHBORS --- #
		count_a = 0
		count_b = 0

		for constraint_pair in constraints[ a ]:
			nbr, constraint = constraint_pair
			if nbr in assignments:
				continue
			count_a += 1
		for constraint_pair in constraints[ b ]:
			nbr, constraint = constraint_pair
			if nbr in assignments:
				continue
			count_b += 1

		return count_a - count_b

	array = [ node for node in domains if node not in assignments ]
	array.sort( sort_func )
	
	count = array[ 0 ]
	minimums = []
	for i in array:
		if i == count:
			minimums.append( i )
	if len( minimums ) == 1:
		return minimums[ 0 ]

	minimum.sort( sort_func2 )
	return minimum[ 0 ]
