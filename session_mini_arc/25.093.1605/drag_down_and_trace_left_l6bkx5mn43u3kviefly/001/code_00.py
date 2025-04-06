import numpy as np
import copy

"""
Transforms an input grid based on the location of zeros.

1. Initialize the output grid as a copy of the input grid.
2. Find all locations (row, column) where the input grid has a value of 0.
3. For each location (r, c) found in step 2, change the value at output_grid[r, c] to 5.
4. For each location (r, c) found in step 2, check if a cell exists directly below it (at row r+1).
5. If a cell exists below (r+1, c), change the value at output_grid[r+1, c] to 0. This overrides any change made in step 3 if the cell at (r+1, c) was also initially 0.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D list or numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid)
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape

    # Find coordinates of all cells with value 0 in the input grid
    zero_locations = []
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 0:
                zero_locations.append((r, c))

    # First pass: Change original zero locations to 5 in the output grid
    for r, c in zero_locations:
        output_grid[r, c] = 5
        
    # Second pass: Change the cell directly below an original zero location to 0
    # This pass happens *after* the first pass, ensuring the 'below' rule
    # takes precedence and overwrites any '5' placed in a cell that was
    # both originally 0 and also below another 0.
    for r, c in zero_locations:
        # Check if there is a row below the current zero location
        if r + 1 < height:
            # Change the cell below to 0 in the output grid
            output_grid[r + 1, c] = 0

    return output_grid.tolist() # Return as list of lists to match example format if needed, or keep as numpy array
