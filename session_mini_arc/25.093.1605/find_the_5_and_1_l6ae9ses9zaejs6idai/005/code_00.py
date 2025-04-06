import numpy as np

"""
Transforms a 5x5 grid based on the following rules:
1. Find the column index 'j' where all cells have the value 5.
2. If such a column 'j' is found:
   a. Change all cells in column 'j' of the output grid to 1.
   b. Determine a target column index 'k' based on 'j':
      i. If j is 2 (the middle column), k is 4 (the last column).
      ii. Otherwise, k is 4 - j (reflection across the vertical center).
   c. Change the cell in the last row (row 4) and column 'k' of the output grid to 2.
3. All other cells in the output grid retain their values from the input grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
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
    if rows != 5 or cols != 5:
        # Handle potential non-5x5 grids if necessary, or raise error
        # For this problem, we assume 5x5 based on examples
        pass 
        
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

    # If an all-5s column was found (target_col_j is not -1)
    if target_col_j != -1:
        # a. Change all cells in the target column 'j' to 1 in the output grid
        output_grid[:, target_col_j] = 1
        
        # b. Determine the target column 'k' for placing the '2'
        target_col_k = -1
        if target_col_j == 2: # Middle column index
            target_col_k = 4 # Last column index
        else:
            target_col_k = (cols - 1) - target_col_j # Reflected column index (4-j for 5x5)
            
        # c. Change the cell in the last row (index rows-1) and column 'k' to 2
        # Ensure target_col_k was set correctly (should always be if target_col_j != -1)
        if target_col_k != -1:
             output_grid[rows - 1, target_col_k] = 2

    # Convert the NumPy array back to a list of lists before returning
    return output_grid.tolist()