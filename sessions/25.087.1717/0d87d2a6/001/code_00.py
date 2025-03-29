import numpy as np

"""
Transforms the input grid by changing red (2) pixels to blue (1) if they are located in the same column below the highest blue (1) pixel in that column.

1. Initialize the output grid as a copy of the input grid.
2. Iterate through each column of the input grid.
3. For the current column, find the row index of the topmost blue pixel (color 1), if any exists.
4. If a topmost blue pixel is found in the current column at row `top_blue_row`:
    a. Iterate through all rows *below* `top_blue_row` in the same column.
    b. If a pixel in this column at a row `r` (where `r > top_blue_row`) has the color red (2) in the input grid, change its color to blue (1) in the output grid.
5. If no blue pixel exists in the current column, make no changes to that column in the output grid.
6. Return the modified output grid.
"""

def find_topmost_pixel(column, color_value):
    """Finds the row index of the first occurrence of a specific color in a column."""
    try:
        # np.where returns a tuple of arrays; we want the first element of the first array
        indices = np.where(column == color_value)[0]
        if len(indices) > 0:
            return indices[0]  # Return the index of the first occurrence (topmost)
        else:
            return None # Color not found in this column
    except IndexError:
        return None # Should not happen with np.where but good practice

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Changes red pixels below the topmost blue pixel in each column to blue.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    num_rows, num_cols = input_np.shape

    # Iterate through each column
    for col_idx in range(num_cols):
        # Extract the current column
        column = input_np[:, col_idx]
        
        # Find the row index of the topmost blue pixel (1) in this column
        top_blue_row = find_topmost_pixel(column, 1) # 1 represents blue

        # If a blue pixel was found in this column
        if top_blue_row is not None:
            # Iterate through the rows below the topmost blue pixel
            for row_idx in range(top_blue_row + 1, num_rows):
                # Check if the pixel in the original input grid at this position is red (2)
                if input_np[row_idx, col_idx] == 2: # 2 represents red
                    # Change the corresponding pixel in the output grid to blue (1)
                    output_grid[row_idx, col_idx] = 1 # 1 represents blue
                    
    # Convert the numpy array back to a list of lists for the standard ARC format
    return output_grid.tolist()
