"""
Transformation Rule:
1. Determine the most frequent pixel color in the input grid (the 'background color').
2. Identify all pixels with the color maroon (9).
3. Define the 'affected area' as the union of all 3x3 neighborhoods centered on each maroon pixel. A neighborhood includes the center pixel and its 8 direct and diagonal neighbors.
4. Create the output grid by copying the input grid.
5. Replace all pixels within the 'affected area' (coordinates identified in step 3) in the output grid with the 'background color' determined in step 1.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Applies the transformation rule to the input grid. Finds all maroon (9)
    pixels, determines the background color (most frequent pixel), and replaces
    the 3x3 neighborhood around each maroon pixel (including the maroon pixel itself)
    with the background color. The neighborhoods are combined (union).

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation and calculations
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    # 1. Determine the most frequent pixel color (background color)
    # Flatten the grid to get a list of all pixel values
    pixels = grid.flatten()
    # Count occurrences of each color and find the most common one
    if not pixels.size: # Handle empty grid case
        return input_grid # Or potentially raise an error or return empty list
    background_color = Counter(pixels).most_common(1)[0][0]

    # 4. Create the output grid by copying the input grid
    # We will modify this copy
    output_grid = grid.copy()

    # 2. Identify the locations of all maroon (9) pixels
    maroon_coords = np.argwhere(grid == 9)

    # 3. Define the 'affected area' as the union of all 3x3 neighborhoods
    # Use a set to automatically handle the union (duplicates)
    affected_coords = set()
    for r, c in maroon_coords:
        # Iterate through the 3x3 neighborhood centered at (r, c)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Calculate the neighbor's coordinates
                nr, nc = r + dr, c + dc
                # Check if the neighbor coordinates are within the grid bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Add valid coordinates to the set
                    affected_coords.add((nr, nc))

    # 5. Replace all pixels within the 'affected area' with the 'background color'
    for r_change, c_change in affected_coords:
        output_grid[r_change, c_change] = background_color

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()