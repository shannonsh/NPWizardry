import random

def solve(num_wizards, num_constraints, wizards, constraints):
    """
    Write your algorithm here.
    Input:
        num_wizards: Number of wizards
        num_constraints: Number of constraints
        wizards: An array of wizard names, in no particular order
        constraints: A 2D-array of constraints, 
                     where constraints[0] may take the form ['A', 'B', 'C']i

    Output:
        An array of wizard names in the ordering your algorithm returns
    """ 

    # number of unsatisfied constraints we're okay with
    max_unsatisfied = 10
    ordering = genSeedOrder(wizards, constraints) 
    num_sat = 0
    while num_sat != num_constraints: 
        # swap
        num_sat = 0
        for const in constraints : 
            if isOrderingValid(ordering, const) : 
                num_sat += 1
            else : 
                # a, b, c = unsatisfied[random.randint(0, len(unsatisfied) - 1)]
                a, b, c = const
                order1 = ordering[:]
                order1[order1.index(c)] = a
                order1[order1.index(a)] = c
                # order1_unsat = len(findUnsatisfied(order1, constraints))
                order2 = ordering[:]
                order2[order2.index(c)] = b
                order2[order2.index(b)] = c
                # order2_unsat = len(findUnsatisfied(order2, constraints))


                num = random.randint(0, 1)
                if num == 0 : 
                    ordering = order1
                else : 
                    ordering = order2
        print(num_sat)
    return ordering
        

def genSeedOrder(wizards, constraints) : 
    random.shuffle(wizards)
    return wizards

def findUnsatisfied(ordering, constraints) : 
    satisfied = 0
    unsatisfied = []
    for const in constraints : 
        isValid = isOrderingValid(ordering, const)
        if isValid : 
            satisfied += 1
        else : 
            unsatisfied.append(const)
    return unsatisfied

def isOrderingValid(ordering, constraint) :
    first = ordering.index(constraint[0])
    second = ordering.index(constraint[1])
    third = ordering.index(constraint[2])
    if (third > first and third < second or third < first and third > second) :
        return False
    return True

