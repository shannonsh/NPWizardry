import networkx as nx
import heapq
import pdb

wiz_const = {}
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
    global wiz_const
    wiz_const = mapConstraints(wizards, constraints)
    partial_soltns = []

    # counter for priority queue since it doesn't allow 
    # identical priorities
    k = 0

    # list of wizards sorted by lowest to highest degree
    sorted_wiz = sortWizByConsts(wiz_const)
    wiz_rankings = {wiz: i for i, wiz in enumerate(sorted_wiz)}

    const_set = set(map(tuple, constraints))
    for i in range(4) : 
        heapq.heappush(partial_soltns, (0, k, nx.DiGraph(), const_set.copy()))
        k += 1

    print("setup done, commencing solving")

    while len(partial_soltns) : 

        # for partial_soltn, const_set in partial_soltns : 
#             partial_soltns.remove(partial_soltn)
        num_seen, _, partial_soltn, const_set = heapq.heappop(partial_soltns)
        const = findNextConst(partial_soltn, const_set, wiz_rankings)
        print("seen " + str(len(partial_soltn)) + "\t num partial_solutions\t" + str(len(partial_soltns)))
        try : 
            const_set.remove(const)
        except KeyError : 
            print("BAD SHIT")
            pass
        possible_arrangements = [(const[0], const[1], const[2]),
                                 (const[2], const[0], const[1]), 
                                 (const[2], const[1], const[0]),
                                 (const[1], const[0], const[2])]
        for arr in possible_arrangements:
            soltn = partial_soltn.copy()
            a, b, c = arr
            if not (soltn.has_node(a) and soltn.has_node(b) and nx.has_path(soltn, a, b)) : 
                soltn.add_edge(a, b)
            if not (soltn.has_node(b) and soltn.has_node(c) and nx.has_path(soltn, b, c)) : 
                soltn.add_edge(b, c)
            # see if we violated any other constraints (seen or not seen)
            is_valid, num_wiz = validNumWiz(soltn, const_set)

            if is_valid and len(list(nx.simple_cycles(soltn))) == 0 :
                heapq.heappush(partial_soltns, (-len(soltn), k, soltn, const_set.copy()))
                k += 1
                # are we done?
                if num_wiz == num_wizards :
                    print("FINAL SOLUTION (found without processing all constraints but validating against them)")
                    ordering = list(nx.topological_sort(soltn))
                    finishEverything(ordering, constraints)
                    return ordering
    if foundCompleteOrdering(heapq.heappop(partial_soltns)) : 
        print("FINAL SOLUTION")
        ordering = list(nx.topological_sort(soltn))
        finishEverything(ordering, constraints)
        return ordering
    print("NO SOLUTION FOUND")
    return ""

"""
Finds the next constraint to process as thus:
"""
def findNextConst(graph, const_set, rankings) : 
    def getRanking(const) : 
        ranking = 0
        return sum([rankings[wiz] for wiz in const]) 

    if (len(graph) == 0 ) : 
        print("popping shit")
        return wiz_const[max(rankings, key=lambda wiz: rankings[wiz])].pop()

    max_const = ()
    max_length = 0
    length = 0

    max_ranking = 0
    max_ranking_const = ()
    for const in const_set : 
        a, b, c = const
        if graph.has_node(a) and graph.has_node(b) : 
            try : 
                length = nx.shortest_path_length(graph, a, b)
            except : 
                length = max_length
        if max_length < length : 
            max_length = length
            max_const = const
        if max_ranking < getRanking(const) : 
            max_ranking_const = const
    if max_const == () : 
        return max_ranking_const # get wiz of highest ranking by sorting ranking dict by ranking
    return max_const
        
def foundCompleteOrdering(graph, constraints) : 
    return isAllValid(graph, constraints, True)

def validNumWiz(graph, constraints) :
    ret = True
    toRemove = []
    for const in constraints :
        validity = isValid(graph, const)
        if not validity :
            ret = False
        if type(validity) != type(True) : 
            toRemove.append(const)
    return ret, len(graph)

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
        return constraint
    return not checkComplete # False if doing full check

   
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
