"""
Construct a 3x3 output grid by selecting pixels from specific locations in a 
5x5 input grid. The mapping is as follows:
Input(0,0) -> Output(0,0)
Input(0,4) -> Output(0,2)
Input(4,0) -> Output(2,0)
Input(4,4) -> Output(2,2)
Input(2,2) -> Output(1,1)
Input(1,1) -> Output(0,1)
Input(1,3) -> Output(1,2)
Input(3,1) -> Output(1,0)
Input(3,3) -> Output(2,1)
"""

import numpy as np

def transform(input_grid):
    """
    Applies the pixel selection and mapping transformation.

    Args:
        input_grid (list of lists or np.array): The 5x5 input grid.

    Returns:
        np.array: The transformed 3x3 output grid.
    """
    # Ensure input is a numpy array for easy indexing
    input_array = np.array(input_grid, dtype=int)

    # Check if input grid is 5x5, though ARC examples guarantee this
    if input_array.shape != (5, 5):
        # Handle error or return empty grid if needed, but for ARC assume valid input
        print("Warning: Input grid is not 5x5") 
        # For robustness, could return None or raise an error
        # return None 

    # Initialize an empty 3x3 output grid (filled with zeros initially)
    output_grid = np.zeros((3, 3), dtype=int)

    # Apply the specific pixel mapping rules
    # Map corners
    output_grid[0, 0] = input_array[0, 0]
    output_grid[0, 2] = input_array[0, 4]
    output_grid[2, 0] = input_array[4, 0]
    output_grid[2, 2] = input_array[4, 4]

    # Map center
    output_grid[1, 1] = input_array[2, 2]

    # Map inner cross to output edges
    output_grid[0, 1] = input_array[1, 1] # Top edge
    output_grid[1, 2] = input_array[1, 3] # Right edge
    output_grid[1, 0] = input_array[3, 1] # Left edge
    output_grid[2, 1] = input_array[3, 3] # Bottom edge

    return output_grid.tolist() # Return as list of lists as per typical ARC output format