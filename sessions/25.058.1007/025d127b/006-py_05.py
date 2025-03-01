"""
The transformation rule identifies contiguous shapes of non-zero pixels in the input grid, 
then removes the "interior" pixels of each shape, leaving only the "border" pixels in the output grid.
A pixel is part of the border if it has at least one orthogonally adjacent neighbor (up, down, left, or right)
that is either a background pixel (color 0) or is outside the bounds of the input grid.
"""

import numpy as np

def find_shapes(grid):
    """
    Identifies and returns a list of shapes within the grid.
    Each shape is a set of (row, col) coordinates.
    """
    shapes = []
    visited = set()
    rows, cols = grid.shape

    def _explore_shape(row, col, current_shape, color):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_shape.add((row, col))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                _explore_shape(row + dr, col + dc, current_shape, color)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and (row, col) not in visited:
                current_shape = set()
                _explore_shape(row, col, current_shape, grid[row, col])
                shapes.append(current_shape)
    return shapes

def find_border(grid, shape):
    """
    Identifies and returns the border pixels of a given shape.
    Checks only orthogonal neighbors.
    """
    border = set()
    rows, cols = grid.shape
    for row, col in shape:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Orthogonal neighbors only
            nr, nc = row + dr, col + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr, nc] == 0:
                border.add((row, col))
                break  # Correct break placement
    return border

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    
    # Find shapes
    shapes = find_shapes(input_grid)
    
    # Find borders and update output_grid
    for shape in shapes:
        border = find_border(input_grid, shape)
        for row, col in border:
            output_grid[row, col] = input_grid[row, col]
    return output_grid