"""
Transforms an input grid based on neighbor-dependent color changes, combining rules derived from two examples.

General Context:
The transformation involves changing colors of pixels based on their eight immediate neighbors.  Rules are applied simultaneously to all pixels.

Specific Transformation Rules:

Example 1 Specifics:
    1. If a pixel is yellow (4) and is immediately to the left of magenta (6), it changes to magenta (6).
    2. If a pixel is yellow (4) and is between two other yellow (4) pixels, it changes to magenta (6).
    3. If a pixel is yellow (4) and is next to one or two gray (5) pixels, it becomes gray (5).
    4. If a yellow (4) pixel has a red (2) neighbor, it does not turn into gray (5).
    5. If a pixel is magenta (6) and to the right of Yellow (4), change to gray (5).
    6. Yellow (4) can become red (2) - conditions not clear.

Example 2 Specifics:
    1. If a pixel is white (0) and *not* adjacent to maroon (9) by any edge, it changes to green (3).
    2. If white (0) is adjacent to maroon (9) vertically or horizontally, do not change to green.
    3. White (0) can become Yellow (4) or Maroon (9) - conditions are not clear.
    4. Maroon(9) remain unchanged.

Combined:
   1. Consider all eight neighbors.
   2. Color changes are conditional and prioritized.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets all eight neighbors of a pixel, including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            current_color = input_grid[row, col]
            neighbors = get_neighbors(input_grid, row, col)
            left_neighbor = input_grid[row, col - 1] if col > 0 else None
            right_neighbor = input_grid[row, col + 1] if col < cols - 1 else None

            # Example 1 Rules
            if current_color == 4:
                if right_neighbor == 6:
                    output_grid[row, col] = 6  # Rule 1
                elif left_neighbor == 4 and right_neighbor == 4:
                    output_grid[row,col] = 6 # Rule 2.
                elif 5 in neighbors:
                    if 2 not in neighbors:
                      output_grid[row,col] = 5 # Rule 3 and 4
                    else:
                       # Rule 6:  4 can become 2, we don't have the rule.
                       pass

            elif current_color == 6:
                if left_neighbor == 4:
                    output_grid[row, col] = 5  # Rule 5

            # Example 2 Rules
            if current_color == 0:
                if 9 not in neighbors:  # diagonals.
                    output_grid[row, col] = 3  # Rule 1
                # Rule 2, 3 are not fully defined.
                else:
                    # do not apply rule 1 if adjacent to a 9
                    pass

            # Rule 4 - maroon remains.
    return output_grid