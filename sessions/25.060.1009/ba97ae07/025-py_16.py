# Hypothetical Code - this would be used to determine the metrics, but
# cannot be run by me directly.

import numpy as np

def analyze_differences(input_grid, expected_output, actual_output):
    differences = []
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            if expected_output[i, j] != actual_output[i, j]:
                differences.append({
                    'row': i,
                    'col': j,
                    'expected': expected_output[i, j],
                    'actual': actual_output[i, j],
                    'input': input_grid[i,j],
                    'neighbors': get_neighbors(input_grid, i, j) # Get surrounding pixel values
                })
    return differences

def get_neighbors(grid, row, col):
    rows, cols = grid.shape
    neighbors = {}
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors[f'({i},{j})'] = grid[i, j]
    return neighbors

# Example of what I would do for *each* example:
# differences = analyze_differences(input_grid, expected_output, actual_output)
# print(differences) # and then summarize in the report