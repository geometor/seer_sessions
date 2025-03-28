"""
Transforms a 3x3 input grid into a 5x5 output grid by selectively duplicating rows and columns.
Specifically:
1. Create an intermediate 5x3 grid by vertically scaling the input:
   - The first row of the input is copied to the first two rows of the intermediate grid.
   - The second row of the input is copied to the third row of the intermediate grid.
   - The third row of the input is copied to the last two rows of the intermediate grid.
2. Create the final 5x5 output grid by horizontally scaling the intermediate 5x3 grid:
   - The first column of the intermediate grid is copied to the first two columns of the output grid.
   - The second column of the intermediate grid is copied to the third column of the output grid.
   - The third column of the intermediate grid is copied to the last two columns of the output grid.
This results in corner pixels of the input mapping to 2x2 blocks, edge pixels mapping to 1x2 or 2x1 blocks, and the center pixel mapping to a 1x1 block in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the described 3x3 to 5x5 scaling transformation.

    Args:
        input_grid (list[list[int]]): A 3x3 grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed 5x5 grid.
    """
    # Convert input list of lists to a numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    
    # Get input dimensions (expected to be 3x3)
    input_height, input_width = input_np.shape
    
    # Define output dimensions
    output_height = 5
    output_width = 5

    # --- Step 1: Vertical Scaling (3x3 -> 5x3) ---
    # Initialize the intermediate grid
    intermediate_grid = np.zeros((output_height, input_width), dtype=int)
    
    # Copy input row 0 to intermediate rows 0 and 1
    intermediate_grid[0:2, :] = input_np[0:1, :]
    
    # Copy input row 1 to intermediate row 2
    intermediate_grid[2:3, :] = input_np[1:2, :]
    
    # Copy input row 2 to intermediate rows 3 and 4
    intermediate_grid[3:5, :] = input_np[2:3, :]

    # --- Step 2: Horizontal Scaling (5x3 -> 5x5) ---
    # Initialize the final output grid
    output_grid_np = np.zeros((output_height, output_width), dtype=int)
    
    # Copy intermediate column 0 to output columns 0 and 1
    output_grid_np[:, 0:2] = intermediate_grid[:, 0:1]
    
    # Copy intermediate column 1 to output column 2
    output_grid_np[:, 2:3] = intermediate_grid[:, 1:2]
    
    # Copy intermediate column 2 to output columns 3 and 4
    output_grid_np[:, 3:5] = intermediate_grid[:, 2:3]

    # Convert the final numpy array back to a list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid
