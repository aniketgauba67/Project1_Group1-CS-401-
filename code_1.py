import math
import string
import sys
import fileinput

# file format:
# candidates(c) voters(v)
# c1 c2 c3
# C1 C2 C3
# Cn Cn Cn

# example:
# 3 5
# A B C
# A C B
# C A B
# B A C 
# A B C 

candidates = []
voters = 0
ballots = [[]]

ballots_ex = [
    ["A", "B", "C"],
    ["A", "C", "B"],
    ["C", "A", "B"],
    ["B", "A", "C"],
    ["A", "B", "C"]
]

def readFromSTDIN(filename):
    global candidates
    global voters
    global ballots
    
    if filename:    
        with open(filename, 'r') as f:
            lines = f.read().strip().splitlines()
    else:
        lines = sys.stdin.read().strip().splitlines()
        
    cand_num, voters = map(int, lines[0].split())
    ballots = [line.split() for line in lines[1:]]
    print(cand_num, voters, ballots)

    for i in range(cand_num):
        candidates.append(chr(i + 65))

readFromSTDIN("sample.txt")
print("There are: " + str(candidates) + " candidates.")

def pairwise(ballots, a, b):
    # input: 
        # ballots
        # a and b
    # returns the count of a > b or b > a
    a_greater_b, b_greater_a = 0,0
    for v in ballots:
        index_a = v.index(a)
        index_b = v.index(b)
        if index_a < index_b:
            a_greater_b += 1
        else:
            b_greater_a += 1

    return a_greater_b, b_greater_a

print(pairwise(ballots, "A", "B"))

# results = {("A", "B"): (4, 1)} for efficiency ? or {("A", "B"): 3}

def condorcet_calculation(ballots, candidates):
    results = {}
    list_size = len(candidates)
    curr_index = 0
    for c in range(len(candidates) - 1):
        for c1 in range(1, len(candidates)):
            if c + c1 < len(candidates):
                results[(candidates[c], candidates[c + c1])] = pairwise(ballots, candidates[c], candidates[c + c1])
        # curr_index += 1
        # while curr_index < list_size:
        #     if (c + 2) < len(candidates):
        #         if not (candidates[c], candidates[c + 2]) in results:
        #             results[(candidates[c], candidates[c + 2])] = pairwise(ballots, candidates[c], candidates[c + 2])
    print(results)

condorcet_calculation(ballots, candidates)

def dodgson_score(candidate, all_candidates, ballots):
    # input: 
        # candidate: current candidate being check rn
        # all_candidates: list of all candidates to loop through (opponents)
        # ballots: formated .txt file
    # output: dodgson score for the current candidate
    res = []
    swaps = 0

    for opponent in opponents: # handles the current opponent
        # A vs A
        if candidate == opponent:
            continue 
        c_votes, o_votes = pairwise(ballots, candidate, opponent)
        if c_votes < o_votes:
            diff = o_votes - c_votes
            # needed to swap (add here)
            # a swap gives one to candidate, takes one from opponent
            needed = int(diff / 2) + 1

            for ballot in ballots: # handles the current loss
                # smaller index = more preferred
                # diff in index = swaps needed
                if ballot.index(opponent) < ballot.index(candidate):
                    swaps = ballot.index(candidate) - ballot.index(opponent)
                    res.append(swaps)
    return min(res)
    
    
