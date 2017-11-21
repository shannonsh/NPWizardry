import numpy as np
import heapq

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

def solve(num_wiz, num_consts, wizards, consts):
    global wiz_consts
    wiz_consts = mapConstraints(wizards, consts)
    
    partial_soltns = []

    # construct the first partial solutions 
    const = consts.pop(0)
    possible_arrangements = [(const[0], const[1], const[2]), (const[2], const[0], const[1]), (const[2], const[1], const[0]), (const[1], const[0], const[2])]
    for arr in possible_arrangements:
        soltn = {}
        a, b, c = arr
        soltn[a] = set([b, c])
        soltn[b] = set([c])
        partial_soltns.append((-2, soltn, set(consts[1:])))

    # now we go into the main solver
    while len(partial_soltns) > 0:
        _, partial_soltn, remaining_consts = heapq.heappop(partial_soltns)
        degrees = map(lambda k,v: (k, len(v)), partial_soltn.iteritems()) # TODO make faster maybe
        best_wizards = sorted(degrees, key=lambda x: x[1])
        const = []
        for wiz in best_wizards:
            wiz_consts = [const in remaining_consts if wiz in const]
            if len(wiz_consts) > 0:
                const = wiz_consts[0]
                break
        if const is []:
            print("we're done but I don't know what to do right now")
            break
        possible_arrangements = [(const[0], const[1], const[2]), (const[2], const[0], const[1]), (const[2], const[1], const[0]), (const[1], const[0], const[2])]
        for arr in possible_arrangements:
            partial_soltn_ = partial_soltn.copy()
            a, b, c = arr
            partial_soltn_[a].add(b)
            partial_soltn_[a].add(c)
            partial_soltn_[b].add(c)
            
            # test if our new solution breaks anything 
            if isValid(partial_soltn_, constraints):
                deg = max(map(lambda k,v: len(v), partial_soltn_))
                partial_soltns.append((-deg, partial_soltn_))


