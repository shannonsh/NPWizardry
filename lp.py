from scipy.optimize import linprog
import heapq
import pdb

leftover_partial_soltns = []
num_wiz = 0
# maximize x_0
c_vec = []
b_start = [1, -1]

sorted_wiz, wiz_rankings = [], []

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
    num_wiz = num_wizards
    global c_vec
    c_vec = list([1] + [0] * (num_wiz-1))
    wiz_const = mapConstraints(wizards, constraints)
    partial_soltns = []
    seen = set([]) # list of seen wizards

    # list of wizards sorted by lowest to highest degree
    global sorted_wiz, wiz_rankings
    sorted_wiz = sortWizByConsts(wiz_const)
    wiz_rankings = {wiz: i for i, wiz in enumerate(sorted_wiz)}

    for i in range(4) : 
        # x_0 <= 1
        row1 = [1] + [0] * (num_wiz-1)
        # -x_0 <= -1
        row2 = [-1] + [0] * (num_wiz-1)
        partial_soltns.append([row1, row2])

    const_set = set(map(tuple, constraints))
    print("setup done, commencing solving")
    while len(const_set) : 
        const = findNextConst(const_set, seen, wiz_rankings)
        print("const", const)
        const_set.remove(const)
        print("remaining consts\t" + str(len(const_set)) + "\t num partial_solutions\t" + str(len(partial_soltns)))
        for wiz in const : 
            seen.add(wiz)

        if (const == ('Mario', 'Yvaine', 'Wilson')) : 
            pdb.set_trace()
        new_soltns = []
        for partial_soltn in partial_soltns : 
            possible_arrangements = [(const[0], const[1], const[2]),
                                     (const[2], const[0], const[1]), 
                                     (const[2], const[1], const[0]),
                                     (const[1], const[0], const[2])]
            for arr in possible_arrangements:
                soltn = partial_soltn.copy()
                a, b, c = arr
                # a < b => a-b < 0
                row = [0] * num_wiz
                row[wiz_rankings[a]] = 1
                row[wiz_rankings[b]] = -1
                soltn.append(row)
                # b < c => b-c < 0
                row = [0] * num_wiz
                row[wiz_rankings[b]] = 1
                row[wiz_rankings[c]] = -1
                soltn.append(row)

                # to help keep track of which people have been processed 
                # or not:
                # -a <= -1 => a >= 1
                row = [0] * num_wiz
                row[wiz_rankings[a]] = -1
                soltn.append(row)

                # see if we violated any other constraints (seen or not seen)
                if isAllValid(soltn, constraints) : 
                    new_soltns.append(soltn)
                    # are we done?
                    if foundCompleteOrdering(soltn, constraints) : 
                        print("FINAL SOLUTION (found without processing all constraints but validating against them)")
                        return getOrdering(soltn) 
        partial_soltns = new_soltns
    if (len(partial_soltns) == 0) : 
        print("NO SOLUTION FOUND")
        return ""
    if foundCompleteOrdering(partial_soltns[len(partial_soltns)-1], constraints) : 
        print("FINAL SOLUTION")
        return getOrdering(soltn) 
    print("NO SOLUTION FOUND")
    return ""

"""
Finds the next constraint to process as thus:
    Choose the constraint that contains the most elements we have seen so far
        if all else equal, pick the constraint containing wizards of highest degree
    If none of the constraints contain any elements we've seen, return the 
        constraints with the wizards of highest degree (combined sum)
"""
def findNextConst(const_set, seen, rankings) : 
    def getRanking(const) : 
        ranking = 0
        return sum([rankings[wiz] for wiz in const]) 

    max_const = ()
    max_intersect = 0
    max_ranking_const = ()
    max_const_ranking = 0
    for const in const_set : 
        intersect = len(seen.intersection(const))
        const_ranking = getRanking(const)
        if max_intersect < intersect or \
          max_intersect == intersect and const_ranking > getRanking(max_const) : 
            max_intersect = intersect
            max_const = const
        if max_const_ranking < const_ranking : 
            max_const_ranking = const_ranking
            max_ranking_const = const
    if max_const == () : 
        return max_ranking_const
    return max_const
        
def getOrdering(A) : 
    # convert graph into ordering
    b = b_start + [-1] * (len(A) - 2) # -2 for x<=1, -x<=-1
    # interior-point is more efficient but my computer gives shitty warnings
    res = linprog(c_vec, A_ub=A, b_ub=b, method="simplex") 
    if (res['status'] == 0) : 
        x = list(res['x'])
    else : 
        return False
    zipped = list(zip(sorted_wiz, x)) # correlates indices with wiz
    sorted_ordering = sorted(zipped, key=lambda a: a[1])
    # gets ordering of wizards, removing wizards that have
    # no constraints yet (i.e. values = 0)
    ordering = [i[0] for i in sorted_ordering if i[1] != 0]
    return ordering

def foundCompleteOrdering(graph, constraints) : 
    return isAllValid(graph, constraints, True)

def isAllValid(A, constraints, checkComplete=False) : 
    ordering = getOrdering(A)
    # infeasible/unbounded/unsolvable LP
    if (ordering == False) : 
        return ordering
    for const in constraints : 
        if not isOrderingValid(ordering, const, checkComplete) : 
            return False
    return True

def isOrderingValid(ordering, constraint, checkComplete=False) :
        if len(ordering) < 3 : 
            return not checkComplete
        # print("checking", ordering, "against", constraint)
        try : 
            first = ordering.index(constraint[0])
            second = ordering.index(constraint[1])
            third = ordering.index(constraint[2])
        except ValueError : 
            # constraint contains wiz not in ordering
            return not checkComplete
        if (third > first and third < second or third < first and third > second) :
                # print(ordering, "violates ", constraint)
                return False
        return True


# def isValid(graph, constraint, checkComplete=False) : 
#     first, second, third = constraint
#     if graph.has_node(first) and graph.has_node(second) and graph.has_node(third) : 
#         rows = len(graph)
#         c = list(range(num_wiz)
#         b = list(range(rows))
# 
#         return isOrderingValid(graph, constraint)
#     return not checkComplete # False if doing full check

# check if graph does not violate a SINGLE constraint
# return True for cases where constraints mention nodes that do not exist
# Checks by seeing if there is a path between 1st and 2nd wiz that goes through
# 3rd wizard
# def isValid(graph, constraint, checkComplete=False) : 
#     first, second, third = constraint
#     if graph.has_node(first) and graph.has_node(second) and graph.has_node(third) : 
#         if nx.has_path(graph, first, third) and nx.has_path(graph, third, second) or \
#            nx.has_path(graph, second, third) and nx.has_path(graph, third, first) : 
#             return False
#         return True
#     return not checkComplete # False if doing full check

   
def mapConstraints(wizards, constraints) : 
    constraints = list(map(tuple, constraints))
    d = {key: set([]) for key in wizards}
    for c in constraints : 
        for wiz in c : 
            d[wiz].add(c)
    return d

def sortWizByConsts(wiz_const_dict) : 
    return sorted(wiz_const_dict, key=lambda d: len(wiz_const_dict[d]), reverse=False)

def copyConstraintDict(wiz_const_dict) : 
    return {key: wiz_const_dict[key].copy() for key in wiz_const_dict}


# def satisfiedConstraints(ordering, constraints) : 
#     if len(ordering) != num_wiz: 
#         return False
#     numSatisfied = 0
#     for const in constraints : 
#         # print(const)
#         if isOrderingValid(ordering, const) : 
#             numSatisfied += 1
#         # print(isOrderingValid(ordering, const))
# #     print("satisfies " + str(numSatisfied) " constraints, fails " + str(len(constraints)-numSatisfied) + " out of " + str(len(constraints)) + " constraints")
# 
#     return len(constraints) - numSatisfied == 0

def finishEverything(ordering, constraints) : 
    print(ordering) 
    satisfiedConstraints(ordering, constraints)
