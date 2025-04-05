import numpy as np

"""
Transform an input 5x5 grid into an output 5x5 grid.
The transformation involves determining a target row based on the non-zero values in each column of the input grid.
This target row is then replicated to form all rows of the output grid.

1. Determine the target row (a sequence of 5 integers).
2. For each column index j (from 0 to 4):
    a. Scan column j of the input grid.
    b. Find the non-zero integer value present within that column. 
       (Assumes only one distinct non-zero value exists per column if any exist).
    c. Assign this non-zero value as the element at index j in the target row.
3. Construct the 5x5 output grid by repeating the determined target row 5 times.
"""

def find_column_value(column):
    """
    Scans a column (1D array or list) and returns the non-zero value.
    If all values are zero, returns 0. Assumes at most one distinct non-zero value.
    """
    for value in column:
        if value != 0:
            return value
    return 0 # Return 0 if the column contains only zeros

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input grid (list of lists) to a NumPy array for easier column access
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the grid (assuming square grid based on examples)
    grid_size = input_array.shape[0] 
    
    # Initialize the target row
    target_row = []

    # Iterate through each column index
    for j in range(grid_size):
        # Extract the j-th column
        column = input_array[:, j]
        
        # Find the non-zero value in the column (or 0 if all zeros)
        # Using max is a concise way if we assume only one distinct non-zero value > 0
        column_value = np.max(column) 
        
        # Append the found value to the target row
        target_row.append(column_value)

    # Initialize the output grid with the correct dimensions
    # Using np.tile is efficient for replicating the row
    output_array = np.tile(target_row, (grid_size, 1))

    # Convert the NumPy array back to a list of lists if needed for the expected output format
    output_grid = output_array.tolist()

    return output_grid
