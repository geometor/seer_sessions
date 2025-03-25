"""
Transforms a 3x3 input grid into a smaller grid by extracting non-zero elements and replicating them based on their diagonal occurrences.
"""

import numpy as np

def count_diagonal_occurrences(grid, value):
    """Counts the occurrences of a value along all diagonals of a grid."""
    count = 0
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == value:

                is_on_diagonal = False
                # Check main diagonal and off-diagonals
                if i == j:  # Main diagonal
                    is_on_diagonal = True
                if i + j == grid.shape[0] - 1:  # Anti-diagonal
                    is_on_diagonal = True
                # diagonals above and below

                if is_on_diagonal:
                    count += 1
    return count

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    non_zero_values = []
    counts = []

    # 1. Identify Non-Zero Elements and their counts
    for value in np.unique(input_grid):
        if value != 0:
            non_zero_values.append(value)
            counts.append(count_diagonal_occurrences(input_grid, value))

    # 2. Construct Output based on counts
    output_list = []
    for i, value in enumerate(non_zero_values):
        output_list.extend([value] * counts[i])

    output_grid = np.array(output_list)

    return output_grid.tolist()