import sys
import numpy as np


def recursive_formula(sim_upleft, sim_left, sim_up, sub_score, gap_score):
    """

    :param sim_upleft: sim(i-1, j-1) where i is rows index, j is columns index
    :param sim_left: sim(i, j-1), gap on query
    :param sim_up: sim(i-1, j), gap on reference
    :param sub_score: substitution score: either match or mismatch
    :param gap_score: score associated to (null, letter) pair alignment
    :return: optimal_move is {0: oblique, 1: horizontal, 2: vertical}.
             These are the score to add to i, j in order to get best node position
             optimal_score is the score associated to the optimal move
    """

    move1 = sim_upleft + sub_score
    move2 = sim_left + gap_score
    move3 = sim_up + gap_score

    moves = [move1, move2, move3]
    optimal_move = np.argmax(moves)
    optimal_score = moves[optimal_move]

    if optimal_move == 0:
        return 0, optimal_score
    elif optimal_move == 1:
        return 1, 0

    return 2, 0


def backtrack(query, reference, best_moves, sim_graph):

    # Initialized aligned ref and query
    al_ref = ''
    al_query = ''

    # Intialize indices. i is the index for query, j is the index for reference
    i, j = np.unravel_index(sim_graph.argmax(), best_moves.shape)

    # Change on the condition with respect to global alignment
    while sim_graph[i, j] != 0:

        move = best_moves[i, j]

        if move == 0:  # Upleft
            # Update indices
            i -= 1
            j -= 1

            # Update alignments
            al_ref = reference[j] + al_ref
            al_query = query[i] + al_query

        elif move == 1:  # Left
            j -= 1
            al_ref = reference[j] + al_ref
            al_query = '_' + al_query

        else:  # Up
            i -= 1
            al_ref = '_' + al_ref
            al_query = query[i] + al_query

    print(al_query)
    print(al_ref)





def path_graph(query, reference, scores):
    match = int(scores[0])
    mismatch = int(scores[1])
    f_sub = lambda a, b: mismatch if a != b else match  # Substitution score function
    gap_score = int(scores[2])

    # Add 1 since position (0, 0) is not associated to any letter
    sim_graph = np.zeros((len(query) + 1, len(reference) +1))

    # Initialize best moves matrix
    # Encoding: {0: oblique, 1: horizontal, 2: vertical}
    best_moves = np.empty((len(query) + 1, len(reference) +1))
    best_moves[1:, 0] = np.array([2 for _ in range(best_moves.shape[0]-1)])
    best_moves[0, 1:] = np.array([1 for _ in range(best_moves.shape[1]-1)])
    best_moves[0, 0] = -1

    # Initialize 1st row and column with gap scores
    sim_graph[0, :] = np.array([i*gap_score for i in range(sim_graph.shape[1])])
    sim_graph[:, 0] = np.array([i*gap_score for i in range(sim_graph.shape[0])])

    # i, j corresponds to specific letters
    for i in range(0, sim_graph.shape[0]-1):
        for j in range(0, sim_graph.shape[1]-1):
            sim_upleft = sim_graph[i, j]
            sim_left = sim_graph[i+1, j]
            sim_up = sim_graph[i, j+1]
            sub_score = f_sub(query[i], reference[j])  # -1 since we start counting from 1

            optimal_move, optimal_score = recursive_formula(sim_upleft, sim_left, sim_up, sub_score, gap_score)

            sim_graph[i+1, j+1] = optimal_score
            best_moves[i+1, j+1] = optimal_move

    backtrack(query, reference, best_moves, sim_graph)


def main(args):
    query = args[0]
    reference = args[1]
    scores = args[2:]

    path_graph(query, reference, scores)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)