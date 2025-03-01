"""
Transforms a larger, sparse grid into a 3x3 grid by extracting a region centered on a "pivot" element (often value 5), preserving the relative positions of its non-zero neighbors.
"""

import numpy as np

def find_pivot(grid):
    # Find the most likely pivot, prioritizing 5 but falling back to others if necessary.
    # First look for value 5.
    fives = np.argwhere(grid == 5)
    if len(fives) > 0:
        return fives[0]

     # If no 5, consider other non-zero elements
    non_zeros = np.argwhere(grid != 0)
    if len(non_zeros) > 0:
         return non_zeros[0]

    return None  # No pivot found


def get_neighbors(grid, pivot_row, pivot_col):
    # Get the values of the neighbors around the pivot, including 0.
    rows, cols = grid.shape
    neighbors = {}
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Skip the pivot itself
            row = pivot_row + i
            col = pivot_col + j
            if 0 <= row < rows and 0 <= col < cols:
                neighbors[(i, j)] = grid[row, col]
    return neighbors

def transform(input_grid):
    # Convert input to numpy array.
    grid = np.array(input_grid)

    # Find the pivot element.
    pivot_coords = find_pivot(grid)

    if pivot_coords is None:
      return [[]] # Return empty output for unusual situations

    pivot_row, pivot_col = pivot_coords

    # Get neighbors around the pivot.
    neighbors = get_neighbors(grid, pivot_row, pivot_col)

    # Create the 3x3 output grid.
    output_grid = np.zeros((3, 3), dtype=int)

    # Place the pivot in the center.
    output_grid[1, 1] = grid[pivot_row, pivot_col]

    # Place neighbors in the output grid.
    for (row_offset, col_offset), value in neighbors.items():
        output_grid[1 + row_offset, 1 + col_offset] = value

    return output_grid.tolist()