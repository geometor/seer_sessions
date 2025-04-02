"""
Transforms the input grid by processing each row independently.
For each row, finds the horizontal span between the leftmost and rightmost non-white pixels.
If non-white pixels exist in the row, fills the entire span in the output grid's corresponding row 
(from the leftmost to the rightmost non-white pixel's column, inclusive) with the color of those 
non-white pixels. Assumes all non-white pixels within a single row share the same color, based on the examples.
If a row contains only white pixels (value 0), copies it unchanged to the output grid.
"""

import numpy as np

def find_row_bounds(row):
    """
    Finds the indices of non-white pixels and their min/max column index in a single row.
    
    Args:
        row (np.array): A 1D NumPy array representing a single row from the grid.
        
    Returns:
        tuple: (min_col, max_col) if non-white pixels are found, otherwise (None, None).
               min_col is the index of the leftmost non-white pixel.
               max_col is the index of the rightmost non-white pixel.
    """
    # Find column indices where the pixel value is not 0 (non-white)
    non_white_indices = np.where(row != 0)[0]
    
    # Check if any non-white pixels were found
    if non_white_indices.size > 0:
        # Find the minimum (leftmost) and maximum (rightmost) indices
        min_col = np.min(non_white_indices)
        max_col = np.max(non_white_indices)
        return min_col, max_col
    else:
        # Return None if the row is all white
        return None, None

def transform(input_grid):
    """
    Applies a row-wise transformation to fill horizontal segments between non-white pixels.

    Args:
        input_grid (list[list[int]]): The input 2D grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed 2D grid as a list of lists.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid.
    # This handles rows with only white pixels correctly by default, as they require no changes.
    output_grid = input_grid_np.copy()
    
    # Get the number of rows (height) in the grid
    height = input_grid_np.shape[0]

    # Iterate through each row of the grid using its index 'r'
    for r in range(height):
        # Get the current row from the input grid
        row = input_grid_np[r, :]
        
        # Find the bounds (min/max column indices) of non-white pixels in this row
        min_col, max_col = find_row_bounds(row)

        # Check if non-white pixels were found (i.e., min_col is not None)
        if min_col is not None:
            # Determine the fill color. Based on examples, we use the color
            # of the leftmost non-white pixel found in the original row.
            fill_color = row[min_col] 
            
            # Fill the segment in the output grid's corresponding row.
            # The slice `min_col : max_col + 1` includes columns from min_col up to max_col.
            output_grid[r, min_col : max_col + 1] = fill_color
            
    # Convert the final NumPy array back to a list of lists for the return value
    return output_grid.tolist()