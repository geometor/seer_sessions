"""
Transformation Rule:
1. Determine the most frequent pixel color in the input grid (the 'background color').
2. Identify all pixels with the color maroon (9).
3. For each maroon pixel, identify its location and the locations of its 8 immediate neighbors (horizontal, vertical, and diagonal).
4. Create a set of all these identified locations (the maroon pixel itself and its valid neighbors within the grid boundaries).
5. Create the output grid by copying the input grid.
6. For every location in the set identified in step 4, change the corresponding pixel in the output grid to the 'background color' determined in step 1.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    # 1. Determine the most frequent pixel color (background color)
    pixels = grid.flatten()
    background_color = Counter(pixels).most_common(1)[0][0]

    # 2. Initialize the output grid as a copy of the input grid
    output_grid = grid.copy()

    # 3. Identify the locations of all maroon (9) pixels
    maroon_coords = np.argwhere(grid == 9)

    # 4. Create a set of all coordinates to be changed
    affected_coords = set()
    for r, c in maroon_coords:
        # Add the maroon pixel itself
        affected_coords.add((r, c))
        # Iterate through its 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Skip the center pixel itself (already added)
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                # Check if the neighbor is within grid bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    affected_coords.add((nr, nc))

    # 5. & 6. Modify the output grid: change affected pixels to background color
    for r_change, c_change in affected_coords:
        output_grid[r_change, c_change] = background_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()