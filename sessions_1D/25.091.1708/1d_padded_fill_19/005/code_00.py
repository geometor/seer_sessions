"""
Transforms the input grid by processing each row independently.
For each row, finds the horizontal span between the leftmost and rightmost non-white pixels.
If non-white pixels exist in the row, fills the entire span in the output grid's corresponding row 
(from the leftmost to the rightmost non-white pixel's column, inclusive) with the color of those 
non-white pixels. Assumes all non-white pixels within a single row share the same color, based on the examples.
If a row contains only white pixels (value 0), copies it unchanged to the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a row-wise transformation to fill horizontal segments.

    Args:
        input_grid (list[list[int]]): The input 2D grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid.
    # This ensures rows with only white pixels are handled correctly by default.
    output_grid = input_grid_np.copy()
    
    # Get the dimensions of the grid
    height, width = input_grid_np.shape

    # Iterate through each row of the grid using its index 'r'
    for r in range(height):
        # Get the current row from the input grid
        row = input_grid_np[r, :]
        
        # Find the column indices of all non-white pixels (value != 0) in this row
        # np.where returns a tuple of arrays (one for each dimension), we need the first element [0]
        non_white_indices = np.where(row != 0)[0]

        # Check if any non-white pixels were found in this row
        if non_white_indices.size > 0:
            # Find the minimum column index (leftmost non-white pixel)
            min_col = np.min(non_white_indices)
            # Find the maximum column index (rightmost non-white pixel)
            max_col = np.max(non_white_indices)
            
            # Determine the fill color. Based on examples, all non-white pixels
            # in a row that needs filling have the same color. We can safely pick the
            # color of the leftmost non-white pixel found.
            fill_color = row[min_col] 
            
            # Fill the segment in the output grid's corresponding row
            # The slice `min_col : max_col + 1` includes columns from min_col up to max_col.
            output_grid[r, min_col : max_col + 1] = fill_color
            
    # Convert the final NumPy array back to a list of lists for the return value
    return output_grid.tolist()
