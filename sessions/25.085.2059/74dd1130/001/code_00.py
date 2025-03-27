import numpy as np

"""
The transformation rule is a matrix transposition. 
The pixel at coordinate (row, col) in the input grid is moved to coordinate 
(col, row) in the output grid. The dimensions of the grid might change 
if the input is not square, with the output height being the input width, 
and the output width being the input height.
"""

def transform(input_grid):
    """
    Transposes the input grid.
    
    Args:
        input_grid (list of lists of int): The input grid represented as a 2D list.
        
    Returns:
        list of lists of int: The transposed output grid.
    """
    # Convert input to numpy array for easier handling, though not strictly necessary
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    input_height, input_width = input_array.shape
    
    # Initialize the output grid with swapped dimensions, filled with a placeholder (e.g., 0)
    # The output height is the input width, and the output width is the input height
    output_grid = [[0 for _ in range(input_height)] for _ in range(input_width)]
    
    # Iterate through each cell of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the value from the input grid at (r, c)
            value = input_array[r, c]
            # Place the value into the output grid at the transposed position (c, r)
            output_grid[c][r] = value
            
    return output_grid
