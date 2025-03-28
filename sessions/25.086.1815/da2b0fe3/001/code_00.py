"""
Identifies if there are exactly two connected objects of the same non-white color
in the input grid. These two objects must be separated by exactly one row or one
column consisting entirely of white pixels (0). If such a configuration is found,
the separating row or column is filled entirely with green pixels (3) in the
output grid. Otherwise, the output grid is identical to the input grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def transform(input_grid):
    """
    Transforms the input grid based on the described rule.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    h, w = grid.shape
    # Initialize output grid as a copy of the input
    output_grid = np.copy(grid)

    # Find unique non-white colors present in the grid
    unique_colors = np.unique(grid[grid != 0])

    # Iterate through each unique non-white color found
    for color in unique_colors:
        # Create a mask for the current color
        mask = (grid == color)
        
        # Label connected components (objects) of the current color
        labeled_array, num_labels = label(mask)

        # Check if exactly two objects of this color were found
        if num_labels == 2:
            # Find the slices representing the bounding boxes of the two objects
            slices = find_objects(labeled_array)
            
            # Ensure we have exactly two slices
            if len(slices) != 2:
                continue 

            slice1, slice2 = slices[0], slices[1]

            # Extract bounding box coordinates (inclusive)
            r1_min, r1_max_incl = slice1[0].start, slice1[0].stop - 1
            c1_min, c1_max_incl = slice1[1].start, slice1[1].stop - 1
            r2_min, r2_max_incl = slice2[0].start, slice2[0].stop - 1
            c2_min, c2_max_incl = slice2[1].start, slice2[1].stop - 1

            # --- Check for Horizontal Separation ---
            # Ensure objects are one above the other, potentially swapping for consistent order
            if r1_min > r2_min:
                # Swap coordinates if obj1 is below obj2
                r1_min, r1_max_incl, r2_min, r2_max_incl = r2_min, r2_max_incl, r1_min, r1_max_incl
                c1_min, c1_max_incl, c2_min, c2_max_incl = c2_min, c2_max_incl, c1_min, c1_max_incl
                
            # Check if there is exactly one row between the objects
            if r2_min == r1_max_incl + 2:
                sep_row_idx = r1_max_incl + 1
                # Check if the separating row contains only white pixels (0)
                if np.all(grid[sep_row_idx, :] == 0):
                    # Fill the entire separating row with green (3)
                    output_grid[sep_row_idx, :] = 3
                    # Return the modified grid as a list of lists
                    return output_grid.tolist()

            # --- Check for Vertical Separation ---
            # Ensure objects are side-by-side, potentially swapping for consistent order
            if c1_min > c2_min:
                 # Swap coordinates if obj1 is right of obj2
                r1_min, r1_max_incl, r2_min, r2_max_incl = r2_min, r2_max_incl, r1_min, r1_max_incl
                c1_min, c1_max_incl, c2_min, c2_max_incl = c2_min, c2_max_incl, c1_min, c1_max_incl

            # Check if there is exactly one column between the objects
            if c2_min == c1_max_incl + 2:
                sep_col_idx = c1_max_incl + 1
                # Check if the separating column contains only white pixels (0)
                if np.all(grid[:, sep_col_idx] == 0):
                    # Fill the entire separating column with green (3)
                    output_grid[:, sep_col_idx] = 3
                    # Return the modified grid as a list of lists
                    return output_grid.tolist()

    # If no such pattern was found for any color, return the original grid copy
    return output_grid.tolist()