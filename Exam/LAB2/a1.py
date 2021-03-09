import sys
import numpy as np


def recursive_formula(i, j, path_graph, query, reference,
                      match_score, mis_score, gap_score):
    row = i+1
    col = j+1

    # h = horizontal, v = vertical, d = diagonal
    d_score = path_graph[row-1, col-1]  # sim(i-1, j-1)
    h_score = path_graph[row, col-1]  # sim(i, j-1)
    v_score = path_graph[row-1, col]  # sim(i-1, j)

    match = query[i] == reference[j]
    if match:
        sub_score = match_score
    else:
        sub_score = mis_score

    scores = [
        d_score + sub_score,
        h_score + gap_score,
        v_score + gap_score
    ]

    best_moves = {
        0:'d',
        1:'h',
        2:'v'
    }

    sim_ij = max(scores)

    traceback = []
    for i in range(3):
        if sim_ij == scores[i]:
            traceback.append(best_moves[i])

    return sim_ij, traceback


def optimal_sol(traceback_matrix, query, reference):
    i, j = len(query)-1, len(reference)-1
    row = i+1
    col = j+1

    q_align = ''
    r_align = ''

    while traceback_matrix[row][col][0] is not None:
        traceback = traceback_matrix[row][col][0]

        if traceback == 'd':
            q_align = query[i] + q_align
            r_align = reference[j] + r_align
            i -= 1
            j -= 1
            row -= 1
            col -= 1

        elif traceback == 'h':
            q_align = '_' + q_align
            r_align = reference[j] + r_align
            j -= 1
            col -= 1

        elif traceback == 'v':
            q_align = query[i] + q_align
            r_align = '_' + r_align
            i -= 1
            row -= 1

    return q_align, r_align


if __name__ == '__main__':
    args = sys.argv[1:]

    query = args[0]
    reference = args[1]
    match = int(args[2])
    mis_match = int(args[3])
    gap = int(args[4])

    # Instantiate graph path
    path_graph = np.zeros((len(query)+1, len(reference)+1), dtype=np.int32)

    # Initialize boundaries
    row_zero = np.array([i*gap for i in range(len(reference)+1)])
    col_zero = np.array([i*gap for i in range(len(query)+1)])
    path_graph[0, :] = row_zero
    path_graph[:, 0] = col_zero

    # Initialize traceback matrix
    traceback_matrix = np.empty(shape=path_graph.shape,
                                dtype=np.object)
    traceback_matrix[0, 1:] = [['h'] for _ in range(len(reference))]
    traceback_matrix[1:, 0] = [['v'] for _ in range(len(query))]
    traceback_matrix[0, 0] = [None]
    traceback_matrix = traceback_matrix.tolist()

    with open('traceback.txt', 'w+') as f:
        f.write(str(traceback_matrix[0][:]) + '\n')
        for i in range(len(query)):
            row = i+1
            for j in range(len(reference)):
                col = j+1
                sim_ij, traceback = recursive_formula(i, j, path_graph, query, reference,
                                                      match, mis_match, gap)
                path_graph[row, col] = sim_ij
                traceback_matrix[row][col] = traceback

            f.write(str(traceback_matrix[row][:]) + '\n')

    q_align, r_align = optimal_sol(traceback_matrix, query, reference)
    print(q_align)
    print(r_align)
