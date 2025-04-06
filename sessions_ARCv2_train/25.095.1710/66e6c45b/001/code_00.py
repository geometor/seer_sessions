"""
Transforms a 4x4 input grid by taking the values from the central 2x2 subgrid 
(rows 1-2, columns 1-2) and placing them into the four corners of a new 4x4 
output grid, which is otherwise filled with zeros.

Specifically:
- Input[1, 1] goes to Output[0, 0]
- Input[1, 2] goes to Output[0, 3]
- Input[2, 1] goes to Output[3, 0]
- Input[2, 2] goes to Output[3, 3]
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A 4x4 grid represented as a list of lists of integers.

    Returns:
        A 4x4 grid represented as a list of lists of integers, resulting from 
        the transformation.
    """
    # Convert input list of lists to a NumPy array for easier indexing
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions (although they are fixed at 4x4 for this problem)
    rows, cols = input_array.shape 
    
    # 1. Create a new 4x4 grid, initialized entirely with zeros.
    output_array = np.zeros((rows, cols), dtype=int)

    # 2. Identify the value in the input grid at row 1, column 1. 
    #    Place this value into the output_grid at row 0, column 0.
    output_array[0, 0] = input_array[1, 1]

    # 3. Identify the value in the input grid at row 1, column 2. 
    #    Place this value into the output_grid at row 0, column 3.
    output_array[0, cols - 1] = input_array[1, 2] # Use cols-1 for generality

    # 4. Identify the value in the input grid at row 2, column 1. 
    #    Place this value into the output_grid at row 3, column 0.
    output_array[rows - 1, 0] = input_array[2, 1] # Use rows-1 for generality

    # 5. Identify the value in the input grid at row 2, column 2. 
    #    Place this value into the output_grid at row 3, column 3.
    output_array[rows - 1, cols - 1] = input_array[2, 2]

    # 6. Return the output_grid. Convert back to list of lists.
    output_grid = output_array.tolist()
    
    return output_grid
