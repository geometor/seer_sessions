"""
Identify the horizontal yellow (4) separator line in the input grid. 
Extract the subgrid above the separator (Grid A) and the subgrid below the separator (Grid B).
Create an output grid with the same dimensions as Grid A.
For each corresponding pixel position (r, c) in Grid A and Grid B:
- If both pixels are red (2), the output pixel at (r, c) is white (0).
- If both pixels are white (0), the output pixel at (r, c) is white (0).
- If one pixel is red (2) and the other is white (0), the output pixel at (r, c) is green (3).
This is equivalent to a pixel-wise XOR operation where white(0) maps to 0, red(2) maps to 1, 
and the result 0 maps to white(0) and 1 maps to green(3).
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule described above to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)
    
    # Find the row index of the yellow separator line (color 4)
    separator_row_index = -1
    for r in range(input_array.shape[0]):
        if np.all(input_array[r, :] == 4):
            separator_row_index = r
            break
            
    if separator_row_index == -1:
        # Handle cases where the separator is not found, though based on examples it should exist
        # For now, let's raise an error or return the input, depending on expected behavior.
        # Raising an error is safer for debugging.
        raise ValueError("Yellow separator line not found in the input grid.")

    # Extract the upper subgrid (Grid A)
    grid_a = input_array[:separator_row_index, :]
    
    # Extract the lower subgrid (Grid B)
    # Make sure Grid B has the same dimensions as Grid A
    grid_b = input_array[separator_row_index + 1 : separator_row_index + 1 + grid_a.shape[0], :]

    # Check if grid_a and grid_b have the same shape
    if grid_a.shape != grid_b.shape:
         raise ValueError(f"Upper ({grid_a.shape}) and lower ({grid_b.shape}) subgrids must have the same dimensions.")

    # Initialize the output grid with zeros (white)
    output_grid = np.zeros_like(grid_a, dtype=int)
    
    # Get dimensions for iteration
    rows, cols = grid_a.shape

    # Iterate through each pixel position
    for r in range(rows):
        for c in range(cols):
            pixel_a = grid_a[r, c]
            pixel_b = grid_b[r, c]
            
            # Apply the XOR-like logic:
            # Map red(2) to 1, white(0) to 0
            val_a = 1 if pixel_a == 2 else 0
            val_b = 1 if pixel_b == 2 else 0
            
            # Perform XOR
            xor_result = val_a ^ val_b # Equivalent to (val_a != val_b)
            
            # Map result back: 1 -> green(3), 0 -> white(0)
            output_grid[r, c] = 3 if xor_result == 1 else 0
            
            # Alternative explicit logic check:
            # if pixel_a == 2 and pixel_b == 2:
            #     output_grid[r, c] = 0 # Both red -> white
            # elif pixel_a == 0 and pixel_b == 0:
            #     output_grid[r, c] = 0 # Both white -> white
            # else: # One is red(2), the other is white(0)
            #     output_grid[r, c] = 3 # Different -> green
            
    # Convert back to list of lists if necessary for the environment
    return output_grid.tolist()
