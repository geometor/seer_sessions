"""
Fill in the white (0) pixels in the input grid based on a repeating numerical sequence derived from non-white neighbors.

The transformation involves these steps:
1. Initialize the output grid as a copy of the input grid.
2. Determine the maximum non-zero value 'L' in the grid, which defines the sequence range 1 to L.
3. Iteratively scan the grid:
   - For each white pixel (value 0):
     - If the pixel to its left is non-white, fill the white pixel with (left_neighbor_value % L) + 1.
     - Otherwise, if the pixel above it is non-white, fill the white pixel with (top_neighbor_value % L) + 1.
   - Repeat the scan until a full pass makes no changes to the grid.
4. Return the filled grid.
"""

import numpy as np

def transform(input_grid):
    """
    Fills white (0) pixels in a grid based on the sequence defined by non-white neighbors.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: The transformed grid with white pixels filled.
    """
    # Convert input to a NumPy array for easier manipulation
    output_grid = np.array(input_grid, dtype=int)
    rows, cols = output_grid.shape

    # Find the maximum value 'L' to determine the sequence range (1 to L)
    # Handle the edge case where the grid might be all zeros
    max_val = np.max(output_grid)
    if max_val == 0:
        # If the grid is all zeros, return it as is (or handle as per specific rules if needed)
        # Based on examples, there's always a non-zero pattern.
        # If L cannot be determined, maybe return original or raise error.
        # Assuming L must be > 0 based on task description.
        # Let's find the max *non-zero* value if possible. If none, return original.
        non_zero_values = output_grid[output_grid > 0]
        if len(non_zero_values) == 0:
             return input_grid # Or raise ValueError("Cannot determine sequence length L from an all-zero grid.")
        max_val = np.max(non_zero_values)
        
    L = max_val

    # Iteratively fill the white pixels
    while True:
        changed_in_pass = False
        # Iterate through each cell in the grid
        for r in range(rows):
            for c in range(cols):
                # Check if the current cell is white (0)
                if output_grid[r, c] == 0:
                    filled = False
                    # Priority 1: Check the neighbor to the left
                    if c > 0 and output_grid[r, c - 1] != 0:
                        neighbor_value = output_grid[r, c - 1]
                        new_value = (neighbor_value % L) + 1
                        output_grid[r, c] = new_value
                        changed_in_pass = True
                        filled = True # Mark as filled to skip checking 'up'

                    # Priority 2: Check the neighbor above (only if not filled by 'left')
                    if not filled and r > 0 and output_grid[r - 1, c] != 0:
                        neighbor_value = output_grid[r - 1, c]
                        new_value = (neighbor_value % L) + 1
                        output_grid[r, c] = new_value
                        changed_in_pass = True

        # If no changes were made in a full pass, the grid is stable
        if not changed_in_pass:
            break

    # Convert the final NumPy array back to a list of lists
    return output_grid.tolist()
