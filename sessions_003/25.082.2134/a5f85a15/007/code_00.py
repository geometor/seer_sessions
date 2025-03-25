"""
1.  **Identify Diagonals:** Scan the input grid to detect all diagonal lines. A diagonal is defined as two or more adjacent pixels of the same non-zero color, extending in one of two directions: top-left to bottom-right, or top-right to bottom-left.
2.  **Find Intersections:** For each color present in the diagonals, identify the points where *two or more* distinct diagonals of that *same* color intersect. An intersection is a single (row, column) coordinate shared by multiple diagonals of the same color.
3. **Apply Transformation**: Iterate through input grid. If coordinate is in list of intersections, change the pixel color to yellow (4). Otherwise keep original color.
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
    for r in range(rows):
        for c in range(cols):
            for color, intersects in intersections.items():
                if (r, c) in intersects:
                    output_grid[r][c] = 4
                    break # move to the next pixel

    return output_grid