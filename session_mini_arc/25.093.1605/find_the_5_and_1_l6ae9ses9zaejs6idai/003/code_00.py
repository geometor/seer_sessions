import numpy as np

"""
Transforms a 5x5 grid based on the following rules:
1. Find the column where all cells have the value 5. Let the index of this column be 'j'.
2. If such a column 'j' is found:
   a. Change all cells in column 'j' of the output grid to 1.
   b. Determine a target column index 'k' based on the index 'j' using the rule k = 4 - j.
   c. Change the cell in the last row (row 4) and column 'k' of the output grid to 2.
3. All other cells in the output grid retain their values from the input grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 5x5 grid of integers.

    Returns:
        list of lists: The transformed 5x5 grid.
    """
    # Convert input grid to a NumPy array for easier column operations
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # Get the dimensions of the grid (assuming 5x5)
    rows, cols = grid.shape
    
    # Variable to store the index of the all-5s column
    target_col_j = -1 

    # Iterate through each column index to find the all-5s column
    for j in range(cols):
        # Extract the current column
        column = grid[:, j]
        # Check if all elements in the column are 5
        if np.all(column == 5):
            target_col_j = j
            break # Stop searching once the column is found

    # If an all-5s column was found
    if target_col_j != -1:
        # Change all cells in the target column 'j' to 1 in the output grid
        output_grid[:, target_col_j] = 1
        
        # Determine the target column 'k' for placing the '2'
        # k is the reflection of j across the vertical center (index 2)
        # k = 0 if j = 4
        # k = 1 if j = 3
        # k = 2 if j = 2
        # k = 3 if j = 1
        # k = 4 if j = 0
        # This simplifies to k = (cols - 1) - target_col_j
        target_col_k = (cols - 1) - target_col_j
        
        # Change the cell in the last row (index rows-1) and column 'k' to 2
        output_grid[rows - 1, target_col_k] = 2

    # Convert the NumPy array back to a list of lists before returning
    return output_grid.tolist()