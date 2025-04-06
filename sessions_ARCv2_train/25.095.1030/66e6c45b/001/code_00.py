"""
Takes a 4x4 input grid and extracts the central 2x2 subgrid. 
These four values are then placed into the four corner positions 
of a new 4x4 output grid, which is otherwise filled with zeros.
Specifically:
- input[1,1] goes to output[0,0]
- input[1,2] goes to output[0,3]
- input[2,1] goes to output[3,0]
- input[2,2] goes to output[3,3]
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving the central 2x2 subgrid elements
    to the corners of the output grid.

    Args:
        input_grid (list of list of int): A 4x4 grid represented as a list of lists.

    Returns:
        list of list of int: The transformed 4x4 grid.
    """
    # Convert input to numpy array for easier indexing
    input_array = np.array(input_grid)
    
    # Get the dimensions (assuming square grid for simplicity, but good practice)
    rows, cols = input_array.shape 
    
    # Initialize a 4x4 output grid with all values set to 0
    # Using the same dimensions as input for generality, although fixed to 4x4 here
    output_grid = np.zeros_like(input_array) 

    # Identify and copy the central 2x2 subgrid elements to the corners
    # Input[1,1] -> Output[0,0]
    output_grid[0, 0] = input_array[1, 1]
    
    # Input[1,2] -> Output[0,3]
    output_grid[0, cols - 1] = input_array[1, 2] # Use cols-1 for generality
    
    # Input[2,1] -> Output[3,0]
    output_grid[rows - 1, 0] = input_array[2, 1] # Use rows-1 for generality
    
    # Input[2,2] -> Output[3,3]
    output_grid[rows - 1, cols - 1] = input_array[2, 2]

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
