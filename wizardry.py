import numpy as np
import heapq
import networkx as nx


def mapContraints(wizards, constraints) : 
        d = dict.fromkeys(wizards, []) 
        for c in constraints : 
                for wiz in c : 
                        d[wiz].append(c)
        return d

# returns if an ordering is valid given a SINGLE constraint
# TODO rewrite to check against topological sort
def isValid(ordering, constraint) : 
        first = ordering.index(constraint[0])
        second = ordering.index(constraint[1])
        third = ordering.index(constraint[2])
        if (third > first and third < second or third < first and third > second) : 
                return False
        return True

wiz_consts = {}

def graphs_equal(g_1, g_2):
    if set(g_1.nodes()) != set(g_2.nodes()):
        return False
    return all([set(g_1[x]) == set(g_2[x]) for x in g_1.nodes()])

def solve(num_wiz, num_consts, wizards, consts):
    #global wiz_consts
    #wiz_consts = mapConstraints(wizards, consts)
    consts = list(map(tuple, consts))

    partial_soltns = []
    seen_soltns = []

    # construct the first partial solutions 
    const = consts.pop(0)
    possible_arrangements = [(const[0], const[1], const[2]), (const[2], const[0], const[1]), (const[2], const[1], const[0]), (const[1], const[0], const[2])]
    for arr in possible_arrangements:
        soltn = nx.DiGraph()
        a, b, c = arr
        soltn.add_edge(a, b)
        soltn.add_edge(a, c)
        soltn.add_edge(b, c)
        partial_soltns.append((-2, soltn, set(consts[1:])))

    # now we go into the main solver
    while len(partial_soltns) > 0:
        _, partial_soltn, remaining_consts = heapq.heappop(partial_soltns)
        
        seen_soltns.append(partial_soltn)
        degrees = nx.degree(partial_soltn)
        best_wizards = sorted(degrees.iteritems(), key=lambda x: x[1], reverse=True)
        const = []
        for wiz, _ in best_wizards:
            wiz_consts = [const for const in remaining_consts if wiz in const]
            if len(wiz_consts) > 0:
                const = wiz_consts[0]
                break
        if const is []:
            const = remaining_consts[0]
        possible_arrangements = [(const[0], const[1], const[2]), (const[2], const[0], const[1]), (const[2], const[1], const[0]), (const[1], const[0], const[2])]
        new_remaining_consts = [c for c in remaining_consts if c is not const]
        for arr in possible_arrangements:
            partial_soltn_ = partial_soltn.copy()
            a, b, c = arr
            partial_soltn_.add_edge(a, b)
            partial_soltn_.add_edge(a, c)
            partial_soltn_.add_edge(b, c)
            
            # test if our new solution breaks anything 
            if len(list(nx.simple_cycles(partial_soltn_))) == 0:    
                if len(new_remaining_consts) == 0:
                    order = list(nx.topological_sort(partial_soltn_))
                    if len(order) == num_wiz and all([isValid(order, c) for c in constraints]):
                        print('super good thing we found')
                        print(order)
                        return order

                deg = len(nx.degree_histogram(partial_soltn_))
                seen = any([graphs_equal(partial_soltn_, g) for g in seen_soltns])
                if not seen:
                    print('new thing')
                    print(len(partial_soltns))
                    partial_soltns.append((-deg, partial_soltn_, new_remaining_consts))

