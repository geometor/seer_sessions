import numpy as np

"""
Transforms a 3x3 input grid into a 9x9 output grid.

The transformation rule is as follows:
1. Initialize a 9x9 output grid filled with zeros.
2. Conceptually divide the 9x9 output grid into nine 3x3 subgrids.
3. Iterate through each cell (r, c) of the 3x3 input grid.
4. If the value at input_grid[r][c] is 2, then copy the entire 3x3 input grid 
   into the corresponding 3x3 subgrid at position (r, c) within the 9x9 output grid.
   The top-left corner of this subgrid in the output is at (r * 3, c * 3).
5. If the value at input_grid[r][c] is not 2, the corresponding 3x3 subgrid 
   in the output remains filled with zeros.
6. Return the final 9x9 grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the conditional tiling transformation to the input grid.

    Args:
        input_grid: A 3x3 grid represented as a list of lists of integers.

    Returns:
        A 9x9 grid represented as a list of lists of integers, resulting
        from the transformation.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Assuming input is always 3x3 based on examples
    input_height, input_width = 3, 3 
    
    # Calculate output grid dimensions (3 * input height, 3 * input width)
    output_height = input_height * input_height 
    output_width = input_width * input_width
    
    # Initialize the output grid with the background value (0)
    # Using numpy for efficient initialization and slicing
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Check if the current input cell value is the trigger value (2)
            if input_grid_np[r, c] == 2:
                # Calculate the top-left coordinates for placing the input grid 
                # into the corresponding subgrid of the output grid
                output_start_row = r * input_height
                output_start_col = c * input_width
                
                # Copy the entire input grid into the calculated position 
                # in the output grid using numpy slicing
                output_grid[output_start_row : output_start_row + input_height, 
                            output_start_col : output_start_col + input_width] = input_grid_np

    # Convert the resulting numpy array back to a list of lists format for the return value
    return output_grid.tolist()
