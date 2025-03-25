"""
1.  **Find Diagonals:** Identify all diagonal lines within the grid. A diagonal line consists of two or more connected pixels of the same non-zero color, extending in either the top-left to bottom-right or top-right to bottom-left directions.

2.  **Find Intersections:** For each color, determine the points where its diagonals intersect. An intersection is a single coordinate (row, column) where two or more diagonals of the same color meet.

3.  **Conditional Color Change:**  For each intersection point found, check the original color of that pixel in the input grid. If the original color was white (0), change it to yellow (4) in the output grid.

4.  **Preserve Other Pixels:** All other pixels in the input grid that are *not* at an intersection of diagonals, or whose intersection was not white, remain unchanged in the output grid.
"""

import numpy as np

def find_diagonals(grid):
    """Finds coordinates of all diagonal lines of non-zero pixels."""
    diagonals = {}
    rows, cols = len(grid), len(grid[0])

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 0:
                color = grid[i][j]
                if color not in diagonals:
                    diagonals[color] = []

                # Check for diagonals
                diag1 = []
                diag2 = []

                # Diagonal 1 (top-left to bottom-right)
                for k in range(-min(i, j), min(rows - i, cols - j)):
                    if grid[i + k][j + k] == color:
                        diag1.append((i + k, j + k))

                # Diagonal 2 (top-right to bottom-left)
                for k in range(-min(i, cols - 1 - j), min(rows - i, j + 1)):
                    if grid[i + k][j - k] == color:
                         diag2.append((i+k, j-k))
                
                if len(diag1) > 1: # requires at least 2 to be a diagonal
                    diagonals[color].append(diag1)
                if len(diag2) > 1:
                    diagonals[color].append(diag2)

    return diagonals

def find_intersections(diagonals):
    """Finds intersection points for each color."""
    intersections = {}
    for color, lines in diagonals.items():
        color_intersections = []
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                intersection = list(set(lines[i]).intersection(lines[j]))
                if intersection:
                    color_intersections.extend(intersection)  # Add all intersection points
        intersections[color] = list(set(color_intersections)) # make unique
    return intersections

def transform(input_grid):
    """Transforms the input grid according to the diagonal intersection rule."""
    output_grid = np.copy(input_grid)
    rows, cols = len(input_grid), len(input_grid[0])

    diagonals = find_diagonals(input_grid)
    intersections = find_intersections(diagonals)

    # change pixel at intersection to yellow if it was white
    for color, intersects in intersections.items():
        for r, c in intersects:
            if input_grid[r][c] == 0:  # Check original color
                output_grid[r][c] = 4

    return output_grid