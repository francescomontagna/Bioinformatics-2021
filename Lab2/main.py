import numpy as np

from code.args import get_args
from copy import deepcopy


class GlobalAligner():
    def __init__(self, args):
        self.query = args.query
        self.ref = args.reference

        # scores
        self.match = args.match
        self.mismatch = args.mismatch
        self.gap = args.gap

        # Initialize similarity matrix
        self.sim = np.zeros((len(self.query)+1, len(self.ref)+1), dtype = np.int16)
        self.sim[0, :] = np.array([self.gap*i for i in range(len(self.ref)+1)]) # initialize row 0
        self.sim[:, 0] = np.array([self.gap * i for i in range(len(self.query)+1)]) # initialize column one

        # Initialize best moves matrix
        self.best_moves = np.zeros((len(self.query)+1, len(self.ref)+1), dtype = np.int16)
        self.best_moves[0, 1:] += 1  # on the edge last step is always horizontal
        self.best_moves[1:, 0] += 2 # on the edge last step is always vertical
        self.best_moves = self.best_moves[:, :, None].tolist() # unsqueeze


    def step(self, i, j):
        """
        horizontal: insertion on the query
        vertical: insertion on the reference
        """
        s_ij = (lambda i,j: self.match if self.query[i-1] == self.ref[j-1] else self.mismatch)

        # scores associated to each move
        move_1 = self.sim[i-1,j-1] + s_ij(i,j) # diagonal
        move_2 = self.sim[i, j-1] + self.gap # horizontal move, -->
        move_3 = self.sim[i-1, j] + self.gap # vertical move
        moves = np.array([move_1, move_2, move_3])

        max_move = np.max(moves)
        best_moves = np.argwhere(moves == max_move) # return more than one element in case of more than one max
        best_moves = np.squeeze(best_moves, -1).tolist()

        self.best_moves[i][j] = best_moves
        self.sim[i, j] = max_move


    def generate_sim_mat(self):
        # generate similarity matrix, breadth first
        print(self.best_moves[0])
        for i in range(1, len(self.query)+1):
            for j in range(1, len(self.ref)+1):
                self.step(i, j)
            print(self.best_moves[i])


        return(self.sim[-1, -1])

    def merge_alignments(self, alignment:list, subpaths:list):
        """
        :param alignment:
        :param subpaths:
        :return:
        """
        alignments_paths = []
        for s_path in subpaths:
            copy_alignment = deepcopy(alignment)
            current_path = s_path + copy_alignment # equivalent to extend but inth eorder I need
            alignments_paths.append(current_path)

        return alignments_paths


    def align(self, query: str, ref: str, best_moves: list):
        """
        Build alignment at this level of the tree
        :return: level_q_alig:list , level_r_alig:list.
                 Each element of the list contains alignment from a single node
        """

        def horizontal(q_alignment, r_alignment, col):
            col -= 1
            q_alignment = '_' + q_alignment
            r_alignment = ref[col] + r_alignment
            return q_alignment, r_alignment, col

        def vertical(q_alignment, r_alignment, row):
            row -= 1
            q_alignment = query[row] + q_alignment
            r_alignment = '_' + r_alignment
            return q_alignment, r_alignment, row

        def diagonal(q_alignment, r_alignment, pos):
            pos = [el - 1 for el in pos]
            q_alignment = query[pos[0]] + q_alignment
            r_alignment = ref[pos[1]] + r_alignment
            return q_alignment, r_alignment, pos

        # find the final alignments
        pos = [len(query), len(ref)] # rows
        q_alignment = r_alignment = ""
        level_q_alig = level_r_alig = []

        while pos != [0, 0]:
            if len(best_moves[pos[0]][pos[1]]) == 1: # if only one optimal path: base case

                if best_moves[pos[0]][pos[1]][0] == 0: # if diagonal
                    q_alignment, r_alignment, pos = diagonal(q_alignment, r_alignment, pos)

                elif best_moves[pos[0]][pos[1]][0] == 1: # if horizontal
                    q_alignment, r_alignment, pos[1] = horizontal(q_alignment, r_alignment, pos[1])

                else: # else vertical
                    q_alignment, r_alignment, pos[0] = vertical(q_alignment, r_alignment, pos[0])

            else: # if  more than one optimal path, recursion
                q_alignment = [q_alignment]
                r_alignment = [r_alignment]
                available_moves = best_moves[pos[0]][pos[1]]
                for move in available_moves:
                    best_moves[pos[0]][pos[1]] = [move]
                    q_subpaths, r_subpaths = self.align(query[0: pos[0]], ref[0:pos[1]], best_moves)
                    q_alignment.append(q_subpaths)
                    r_alignment.append(r_subpaths)

                return q_alignment, r_alignment

        return [q_alignment], [r_alignment] # base case



def main(args):
    global_aligner = GlobalAligner(args)
    optimal_score = global_aligner.generate_sim_mat()
    print(f"Optimal alignment score: {optimal_score}")
    print(global_aligner.align(global_aligner.query, global_aligner.ref, global_aligner.best_moves))



if __name__ == "__main__":
    args = get_args()
    main(args)


