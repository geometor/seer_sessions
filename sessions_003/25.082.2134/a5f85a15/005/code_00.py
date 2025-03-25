"""
1.  **Identify Diagonals:** Examine the input grid to find all diagonal lines. A diagonal line consists of two or more adjacent pixels of the same non-zero color, extending in either of two directions:
    *   Top-left to bottom-right
    *   Top-right to bottom-left

2.  **Locate Intersections:** For each color present in the diagonals, find the points where two or more of its diagonals intersect. An intersection is a single (row, column) coordinate where diagonals of the same color share a pixel.

3.  **Apply Color Change:** Change the color of *every* intersection point to yellow (4) in the output grid. The original color of the pixel does not matter.

4.  **Preserve Other Pixels:** All pixels in the input grid that are *not* at an intersection of diagonals, remain unchanged in the output grid.
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

    # Find all diagonals in the input grid
    diagonals = find_diagonals(input_grid)
    
    # Find all intersection points of diagonals of the same color
    intersections = find_intersections(diagonals)

    # Change the color of all intersection points to yellow (4)
    for color, intersects in intersections.items():
        for r, c in intersects:
            output_grid[r][c] = 4  # Always change to yellow

    return output_grid