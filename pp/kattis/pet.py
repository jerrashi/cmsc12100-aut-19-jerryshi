import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/pet
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.

# This function takes a single parameters containing a list
# with exactly five entries (one per contestant). Each entry 
# is a list with exactly four integers (the scores for that
# contestant)
def solve(contestant_scores):
    score_list = []
    maximum = 0
    winner = 0
    for row in contestant_scores:
    	for score in row:
    		contestant_score += score
    	score_list.appent(contestant_score)

    for score in score_list:
    	if score > maximum:
    		maximum = score
    		winner = score_list.index(score) + 1

    return winner, maximum


if __name__ == "__main__":
    tokens = sys.stdin.read().strip().split()

    scores = [ [int(tokens.pop(0)) for i in range(4)] for j in range(5) ]

    pet, score = solve(scores)

    print(pet, score)
