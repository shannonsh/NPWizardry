import math 
import random
import time
import pdb

all_constraints = []
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
    global all_constraints
    all_constraints = constraints

    seen = set([])

    # number of unsatisfied constraints we're okay with
    ordering = genSeedOrder(wizards, constraints) 
    best_ordering = ordering
    seen.add(tuple(best_ordering))
    num_sat = 0
    best_sat = 0
    unsat = findUnsatisfied(ordering, constraints)
    best_unsat = len(unsat)

    temp = 1
    # rate of decrease in randomness
    alpha = 0.999
    accept_prob = 1 
    while num_sat < num_constraints: 
        for i in range(500) : 
            ordering = best_ordering
            unsat = findUnsatisfied(ordering, constraints)
            if (len(unsat) == 0) : 
                return ordering
            const = random.choice(unsat)

            #  choose best among all possible places to swap
            a, b, c = const
            aIndex = ordering.index(a)
            bIndex = ordering.index(b)
            cIndex = ordering.index(c)
            poss_spots = list(range(0, min(aIndex, bIndex) + 1)) + list(range(max(aIndex, bIndex), len(ordering)))
            best_swap = ordering
            best_swap_unsat = list(range(num_constraints))
            for spot in poss_spots : 
                order1 = ordering[:]
                order1[cIndex] = ordering[spot]
                order1[spot] = c
                unsat1 = findUnsatisfied(order1, constraints)
                if (len(best_swap_unsat) > len(unsat1)) : 
                    # if ordering seen before, probability of accepting it decreases over time
                    # reduces probability of getting stuck in a local minima
                    if (tuple(order1) not in seen or accept_prob > random.random()) : 
                        best_swap = order1 
                        best_swap_unsat = unsat1
            ordering = best_swap
            unsat = best_swap_unsat

#             order2 = ordering[:]
#             order2[ordering.index(c)] = b
#             order2[ordering.index(b)] = c
#             unsat2 = findUnsatisfied(order2, constraints)
#             if (len(unsat1) < len(unsat2)) : 
#                 ordering = order1
#                 unsat = unsat1
#             else : 
#                 ordering = order2
#                 unsat = unsat2

            num_unsat = len(unsat)
            num_sat = num_constraints - len(unsat)
            # print("ordering", ordering, "satisfies", num_sat)

            if (num_unsat < best_unsat) : 
                print("best_unsat - num_unsat", best_unsat - num_unsat)
                
            # probability of exploring new solutions decreases over time
            accept_prob = math.exp((best_unsat - num_unsat)/math.sqrt(temp))
            # if new solution better than best solution then definitely update
            # best solution
            if accept_prob > random.random() : 
                best_ordering = ordering[:]
                seen.add(tuple(best_ordering))
                best_sat = num_sat
                best_unsat = len(unsat)
                print("best ordering", best_ordering, "satisfies", best_sat)
        temp += 1
    return best_ordering
        
def genSeedOrder(wizards, constraints) : 
    # random.shuffle(wizards)
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

