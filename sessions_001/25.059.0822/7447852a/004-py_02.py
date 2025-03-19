"""
1. Iterate through each row of the input grid.
2. Identify contiguous sequences of red (2) pixels.
3. For each red sequence, examine the *adjacent* white (0) pixels. Adjacency includes horizontal, vertical, and diagonal neighbors.
4. Change the color of all adjacent white pixels to yellow.
5. Stop when a non-white pixel is encountered.
"""

import numpy as np

def get_red_sequences(grid):
    """
    Finds contiguous sequences of red pixels in each row.
    Returns a list of (row, start_col, end_col) tuples.
    """
    red_sequences = []
    rows, cols = grid.shape
    for r in range(rows):
        in_sequence = False
        start_col = -1
        for c in range(cols):
            if grid[r, c] == 2:
                if not in_sequence:
                    in_sequence = True
                    start_col = c
            elif in_sequence:
                in_sequence = False
                red_sequences.append((r, start_col, c - 1))
        if in_sequence:
            red_sequences.append((r, start_col, cols - 1))
    return red_sequences

def get_adjacent_white_pixels(grid, row, col):
    """
    Gets the coordinates of white pixels adjacent to a given cell.
    Considers horizontal, vertical, and diagonal neighbors.
    """
    rows, cols = grid.shape
    adjacent_whites = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                adjacent_whites.append((nr, nc))
    return adjacent_whites

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    red_sequences = get_red_sequences(output_grid)

    for row, start_col, end_col in red_sequences:
        # Collect all adjacent white pixels for the entire sequence
        adjacent_whites = set()
        for c in range(start_col, end_col + 1):
            adjacent_whites.update(get_adjacent_white_pixels(output_grid, row, c))

        # Change the color of adjacent white pixels to yellow
        for r, c in adjacent_whites:
            output_grid[r, c] = 4

    return output_grid