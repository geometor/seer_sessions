import numpy as np

"""
Transforms an input grid by processing each row independently. 
For each row, all magenta (6) pixels are identified and then moved 
to the leftmost positions of that same row in the output grid, 
maintaining their count but not necessarily their original relative order 
(though in this specific transformation, since they are all the same color, 
relative order doesn't matter). 
The rest of the cells in the row become white (0).
"""

def transform(input_grid):
    """
    Applies the row-wise left-consolidation transformation to a grid.

    Args:
        input_grid (list of lists or numpy array): The input grid containing integers 0-9.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_np.shape

    # Initialize output_grid with the same dimensions as input, filled with background color (0)
    output_grid = np.zeros_like(input_np)

    # Process each row independently
    for r in range(num_rows):
        # Get the current row from the input grid
        input_row = input_np[r, :]

        # Count the number of magenta pixels (value 6) in the current row
        magenta_count = np.count_nonzero(input_row == 6)

        # If there are any magenta pixels in this row
        if magenta_count > 0:
            # Place the counted number of magenta pixels at the beginning (left side) of the corresponding row in the output grid
            output_grid[r, :magenta_count] = 6

    return output_grid.tolist() # Return as list of lists per ARC standard
