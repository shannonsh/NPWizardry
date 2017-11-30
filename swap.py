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

    # number of unsatisfied constraints we're okay with
    ordering = genSeedOrder(wizards, constraints) 
    best_ordering = ordering
    num_sat = 0
    best_sat = 0
    unsat = findUnsatisfied(ordering, constraints)
    best_unsat = len(unsat)

    temp = 1
    alpha = 0.99
    while num_sat < num_constraints: 
        for i in range(500) : 
            ordering = best_ordering
            unsat = findUnsatisfied(ordering, constraints)
            if (len(unsat) == 0) : 
                return ordering
            const = random.choice(unsat)

            a, b, c = const
            order1 = ordering[:]
            order1[ordering.index(c)] = a
            order1[ordering.index(a)] = c
            unsat1 = findUnsatisfied(order1, constraints)

            order2 = ordering[:]
            order2[ordering.index(c)] = b
            order2[ordering.index(b)] = c
            unsat2 = findUnsatisfied(order2, constraints)
            if (len(unsat1) < len(unsat2)) : 
                ordering = order1
                unsat = unsat1
            else : 
                ordering = order2
                unsat = unsat2

            num_unsat = len(unsat)
            num_sat = num_constraints - len(unsat)
            # print("ordering", ordering, "satisfies", num_sat)

            if (num_unsat < best_unsat) : 
                print("best_unsat - num_unsat", best_unsat - num_unsat)
                
            accept_prob = math.exp((best_unsat - num_unsat)/math.sqrt(temp))
            if accept_prob > random.random() : 
                best_ordering = ordering[:]
                best_sat = num_sat
                best_unsat = len(unsat)
                print("best ordering", best_ordering, "satisfies", best_sat)
        temp += 1
    return best_ordering
        
def swap(ordering, const) : 
    a, b, c = const
    ordering.remove(c)
    aIndex = ordering.index(a)
    bIndex = ordering.index(b)
    # allNewCIndexes = [aIndex, bIndex]
    ordering.insert(aIndex, c)
    unsat1 = findUnsatisfied(ordering, all_constraints)
    ordering.remove(c)

    ordering.insert(bIndex, c)
    unsat2 = findUnsatisfied(ordering, all_constraints)
    ordering.remove(c)

    if (len(unsat1) < len(unsat2)) : 
        ordering.insert(aIndex, c)
        return unsat1
    else : 
        ordering.insert(bIndex, c)
        return unsat2


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

