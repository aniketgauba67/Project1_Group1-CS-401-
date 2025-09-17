import math
import string
import sys
import fileinput
import time
from collections import defaultdict

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

voters = 0
start_time = time.time()

ballots_ex = [
    ["A", "B", "C"],
    ["A", "C", "B"],
    ["C", "A", "B"],
    ["B", "A", "C"],
    ["A", "B", "C"]
]

def readFromSTDIN(filename, candidates):
    
    global voters

    if filename:    
        with open(filename, 'r') as f:
            lines = f.read().strip().splitlines()
    else:
        lines = sys.stdin.read().strip().splitlines()
        
    cand_num, voters = map(int, lines[0].split())
    ballots = [line.split() for line in lines[1:]]
    # print(cand_num, voters, ballots)

    for i in range(cand_num):
        candidates.append(chr(i + 65))

    return ballots

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

def weighted_majority_graph(ballots, candidates):
    # input: 
        # ballots
        # candidates
    # returns a dictoniary with a pair of candidate and pairwise count
    results = defaultdict(dict)
    list_size = len(candidates)
    curr_index = 0
    for c in range(len(candidates) - 1):
        for c1 in range(1, len(candidates)):
            if c + c1 < len(candidates):
                results[candidates[c]][candidates[c + c1]] = pairwise(ballots, candidates[c], candidates[c + c1])

    return results

def dodgson_score(candidate, all_candidates, ballots):
    # input: 
        # candidate: current candidate being check rn
        # all_candidates: list of all candidates to loop through (opponents)
        # ballots: formated .txt file
    # output: dodgson score for the current candidate
    res = 0 
    swaps = 0

    # needed = int(voters/2) + 1

    for opponent in all_candidates: # handles the current opponent
        # A vs A
        if candidate == opponent:
            continue 
        c_votes, o_votes = pairwise(ballots, candidate, opponent)
        if c_votes < o_votes:
            diff = o_votes - c_votes
            # needed to swap (add here)
            # a swap gives one to candidate, takes one from opponent
            # needed = needed - diff - 1
            needed = int(diff / 2) + 1

            swap_history = []
            for ballot in ballots: # handles the current loss
                # smaller index = more preferred
                # diff in index = swaps needed
                if ballot.index(opponent) < ballot.index(candidate):
                    swaps = ballot.index(candidate) - ballot.index(opponent)
                    swap_history.append(swaps)
            
            # print(str(swap_history) + " for " + str(candidate))

            swap_history.sort()
            cheapest_history = swap_history[:needed]
            res += sum(cheapest_history)

    return res
    
def main():
    filename = input("Please enter the name of the file you're observing: ")

    candidates = []
    ballots = [[]]

    ballots = readFromSTDIN(filename, candidates)
    
    winner = None
    min_score = 999
    min_holder = []
    for c in candidates:
        curr_score = dodgson_score(c, candidates, ballots)
        if curr_score == 0:
            winner = c
            break
        elif curr_score == min_score:
            min_holder.append(c)
        elif curr_score < min_score:
            min_holder.clear()
            min_score = curr_score
            min_holder.append(c)

        print(c + " has a Dodgson's Score of " + str(curr_score))

    if winner:
        print("The Condorcet, and therefore Dodgson's, winner is " + winner + ".")
    else:
        print("The Dodgson's winner(s) is " + str(min_holder) + " with a score of " + str(min_score) + ".")

main()
print("--- %s seconds ---" % (time.time() - start_time))