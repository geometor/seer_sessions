import numpy as np

"""
Transformation Rule:

1. Take the input grid.
2. Separate the first column from the rest of the grid (the subgrid).
3. Find the row index of the red pixel (value 2) in the first column.
4. If the red pixel is in the first row (index 0), the output grid is the subgrid as is.
5. If the red pixel is not in the first row (index > 0), reorder the rows of the subgrid:
    a. Define a split point at row index 3.
    b. The rows from index 3 to the end form the top part of the output.
    c. The rows from index 0 up to (but not including) index 3 form the bottom part of the output.
    d. Concatenate the top part and bottom part vertically.
6. Return the resulting grid.
"""

def find_red_pixel_index(column):
    """Finds the index of the first occurrence of value 2 (red) in a column."""
    indices = np.where(column == 2)[0]
    if len(indices) > 0:
        return indices[0]
    return -1 # Should not happen based on examples, but good practice

def transform(input_grid):
    """
    Removes the first column and reorders the remaining rows based on the 
    position of the red pixel (2) in the original first column.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array
    input_grid_np = np.array(input_grid)
    
    # Separate the first column and the rest of the grid (subgrid)
    first_column = input_grid_np[:, 0]
    subgrid = input_grid_np[:, 1:]
    
    # Find the row index of the red pixel in the first column
    red_index = find_red_pixel_index(first_column)
    
    # Initialize output grid
    output_grid = None
    
    # Check the condition for reordering
    if red_index == 0:
        # If red pixel is at index 0, output is the subgrid unchanged
        output_grid = subgrid
    else:
        # If red pixel is not at index 0, perform the split and reorder
        split_idx = 3 
        
        # Ensure split index is valid for grid height
        if split_idx >= 0 and split_idx <= subgrid.shape[0]: 
             # Rows from split_idx onwards
            top_part = subgrid[split_idx:]
            # Rows before split_idx
            bottom_part = subgrid[:split_idx]
            
            # Concatenate the parts vertically
            output_grid = np.vstack((top_part, bottom_part))
        else:
             # Fallback or error handling if split_idx is out of bounds
             # Based on examples, this shouldn't occur as grids are 6 rows high
             output_grid = subgrid # Default to no reordering if split is invalid

    # Return the resulting grid
    return output_grid.tolist() # Convert back to list of lists if required by spec