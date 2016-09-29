"""Satisfies a set of constraints through a recursive backtracking algorithm."""

def backtracking(domains, assignments, constraints):
    """Backtracks until it finds assignments for every value within each domain following the given
    constraints"""
    if len(assignments) == len(domains):
        return True

    next_var = find_min(domains, assignments, constraints)
    unique_list = []

    def least_constraining_value(alpha, beta):
        """Sorts by the value that will allow the highest number of other values to remain in the
        domains of the neighbor nodes"""
        counter_alpha = 0
        counter_beta = 0
        for constraint_pair in constraints[next_var]:
            nbr, constraint = constraint_pair
            if nbr in assignments:
                continue
            if nbr in unique_list:
                continue
            else:
                unique_list.append(nbr)

            for possible in domains[nbr]:
                if not constraint(next_var, alpha, nbr, possible):
                    counter_alpha += 1

            for possible in domains[nbr]:
                if not constraint(next_var, beta, nbr, possible):
                    counter_beta += 1
        return counter_alpha - counter_beta
    domains[next_var].sort(least_constraining_value)

    for possible_val in domains[next_var]:
        for constraint_pair in constraints[next_var]:
            nbr, constraint = constraint_pair

            if nbr not in assignments:
                continue

            if not constraint(next_var, possible_val, nbr, assignments[nbr]):
                break
        else:
            assignments[next_var] = possible_val

            new_domains = {}
            for i in domains.keys():
                new_domains[i] = domains[i][:]

            for constraint_pair in constraints[next_var]:
                nbr, constraint = constraint_pair

                for possible in domains[nbr]:
                    if possible in new_domains[nbr]:
                        if not constraint(next_var, possible_val, nbr, possible):
                            new_domains[nbr].remove(possible)
            if backtracking(new_domains, assignments, constraints):
                return True
            else:
                del assignments[next_var]
    return False

def find_min(domains, assignments, constraints):
    """Finds the next node to which to attempt to assign a value"""
    def domain_size(alpha, beta):
        """A sort function based on the number of possible remaining values"""
        return len(domains[alpha]) - len(domains[beta])

    def unassigned_neighbors(alpha, beta):
        """A sort function based on the number of neighbor nodes without a value"""
        counter_alpha = 0
        counter_beta = 0

        for constraint_pair in constraints[alpha]:
            nbr, _ = constraint_pair
            if nbr in assignments:
                continue
            counter_alpha += 1
        for constraint_pair in constraints[beta]:
            nbr, _ = constraint_pair
            if nbr in assignments:
                continue
            counter_beta += 1

        return counter_alpha - counter_beta

    array = [node for node in domains if node not in assignments]
    array.sort(domain_size)

    count = array[0]
    minimums = []
    for idx in array:
        if idx == count:
            minimums.append(idx)
    if len(minimums) == 1:
        return minimums[0]

    minimums.sort(unassigned_neighbors)
    return minimums[0]
