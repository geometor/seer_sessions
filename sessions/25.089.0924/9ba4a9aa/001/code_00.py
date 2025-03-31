"""
Identify the background color (most frequent color) in the input grid.
Scan the input grid for a unique 3x3 subgrid pattern where:
1. The central pixel has color 'A'.
2. All 8 surrounding pixels (neighbors, including diagonals) have the same color 'B'.
3. Color 'A' is different from color 'B'.
4. Color 'A' is different from the background color.
5. Color 'B' is different from the background color.
Extract and return this unique 3x3 subgrid.
"""

import numpy as np
from collections import Counter

def _find_background_color(grid_np):
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid_np, return_counts=True)
    background_color = colors[np.argmax(counts)]
    return background_color

def transform(input_grid):
    """
    Identifies and extracts a specific 3x3 pattern from the input grid.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The extracted 3x3 pattern.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Identify Background Color
    background_color = _find_background_color(input_grid_np)

    # 2. Scan for Target Pattern
    # Iterate through possible center points (r, c) of a 3x3 subgrid
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # 3. Analyze Subgrid centered at (r, c)
            center_color = input_grid_np[r, c]

            # Get the 8 neighbors
            neighbors = [
                input_grid_np[r-1, c-1], input_grid_np[r-1, c], input_grid_np[r-1, c+1],
                input_grid_np[r,   c-1],                     input_grid_np[r,   c+1],
                input_grid_np[r+1, c-1], input_grid_np[r+1, c], input_grid_np[r+1, c+1]
            ]

            # Check if all neighbors are the same color
            first_neighbor_color = neighbors[0]
            all_neighbors_same = all(n == first_neighbor_color for n in neighbors)

            if all_neighbors_same:
                border_color = first_neighbor_color

                # Check conditions:
                # a. Center color != border color
                # b. Center color != background color
                # c. Border color != background color
                if (center_color != border_color and
                    center_color != background_color and
                    border_color != background_color):

                    # 4. Extract and Output the 3x3 subgrid
                    # The top-left corner of the 3x3 subgrid is (r-1, c-1)
                    output_grid = input_grid_np[r-1:r+2, c-1:c+2]
                    # Convert back to list of lists format if required by the environment
                    return output_grid.tolist()

    # Should not happen based on task description, but return something
    # Return the original grid or an empty grid as a fallback
    # For ARC, returning the input might indicate failure or no change.
    # Let's return an empty list for clarity of failure to find the pattern.
    print("Warning: Target pattern not found.")
    return []