import networkx as nx
import heapq

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
    wiz_const = mapConstraints(wizards, constraints)
    partial_soltns = []
    seen = set([]) # list of seen wizards

    # list of wizards sorted by lowest to highest degree
    sorted_wiz = sortWizByConsts(wiz_const)
    wiz_rankings = {wiz: i for i, wiz in enumerate(sorted_wiz)}

    for i in range(4) : 
        partial_soltns.append(nx.DiGraph())

    const_set = set(map(tuple, constraints))
    print("setup done, commencing solving")

    while len(const_set) : 
        const = findNextConst(const_set, seen, wiz_rankings)
        print("const", const)
        const_set.remove(const)
        print("remaining consts\t" + str(len(const_set)) + "\t num partial_solutions\t" + str(len(partial_soltns)))
        for wiz in const : 
            seen.add(wiz)

        new_soltns = []
        for partial_soltn in partial_soltns : 
            partial_soltns.remove(partial_soltn)
            possible_arrangements = [(const[0], const[1], const[2]),
                                     (const[2], const[0], const[1]), 
                                     (const[2], const[1], const[0]),
                                     (const[1], const[0], const[2])]
            for arr in possible_arrangements:
                soltn = partial_soltn.copy()
                a, b, c = arr
                soltn.add_edge(a, b)
                soltn.add_edge(b, c)
                # see if we violated any other constraints (seen or not seen)
                if isAllValid(soltn, constraints) and len(list(nx.simple_cycles(soltn))) == 0 : 
                    new_soltns.append(soltn)
                # are we done?
                if foundCompleteOrdering(soltn, constraints) and len(list(nx.simple_cycles(soltn))) == 0 : 
                    print("FINAL SOLUTION (found without processing all constraints but validating against them)")
                    ordering = list(nx.topological_sort(soltn))
                    finishEverything(ordering, constraints)
                    return ordering
        partial_soltns = new_soltns
    if foundCompleteOrdering(partial_soltns[len(partial_soltns)-1]) : 
        print("FINAL SOLUTION")
        ordering = list(nx.topological_sort(soltn))
        finishEverything(ordering, constraints)
        return ordering
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
        
def foundCompleteOrdering(graph, constraints) : 
    return isAllValid(graph, constraints, True)

def isAllValid(graph, constraints, checkComplete=False) : 
    for const in constraints : 
        if not isValid(graph, const, checkComplete) :
            return False
    return True

# check if graph does not violate a SINGLE constraint
# return True for cases where constraints mention nodes that do not exist
def isValid(graph, constraint, checkComplete=False) : 
    first, second, third = constraint
    if graph.has_node(first) and graph.has_node(second) and graph.has_node(third) : 
        if nx.has_path(graph, first, third) and nx.has_path(graph, third, second) or \
           nx.has_path(graph, second, third) and nx.has_path(graph, third, first) : 
            return False
        return True
    return not checkComplete # False if doing full check

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


def isOrderingValid(ordering, constraint) :
        first = ordering.index(constraint[0])
        second = ordering.index(constraint[1])
        third = ordering.index(constraint[2])
        if (third > first and third < second or third < first and third > second) :
                return False
        return True

def satisfiedConstraints(ordering, constraints) : 
    for const in constraints : 
        print(const)
        print(isOrderingValid(ordering, const))

def finishEverything(ordering, constraints) : 
    print(ordering) 
    satisfiedConstraints(ordering, constraints)
