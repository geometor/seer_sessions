import numpy as np

"""
Identifies contiguous horizontal blocks of red (2) pixels in the input grid.
Transforms these red blocks based on their length:
- If the length of a red block is odd, change its pixels to blue (1).
- If the length of a red block is even, change its pixels to azure (8).
White (0) pixels remain unchanged.
The input and output grids have the same dimensions (1x20).
"""

def transform(input_grid):
    """
    Transforms red blocks in a 1D grid based on their length parity.

    Args:
        input_grid (np.array): A 1xN numpy array containing 0s and 2s.

    Returns:
        np.array: A 1xN numpy array with red blocks transformed to blue (1)
                  or azure (8) based on odd or even length respectively.
    """
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # We expect a 1xN grid based on examples
    if height != 1:
        # Handle potential unexpected input dimensions if necessary,
        # but based on examples, we assume height is 1.
        # For now, we proceed assuming height is 1.
        pass 

    # Iterate through the single row to find red blocks
    i = 0
    while i < width:
        # Check if the current pixel is red (2)
        if input_grid[0, i] == 2:
            # Found the start of a potential red block
            start_index = i
            
            # Find the end of the contiguous red block
            j = i
            while j < width and input_grid[0, j] == 2:
                j += 1
            
            # Calculate the length of the red block
            length = j - start_index
            
            # Determine the output color based on whether the length is odd or even
            if length % 2 != 0: # Odd length
                output_color = 1 # Blue
            else: # Even length
                output_color = 8 # Azure
                
            # Update the corresponding pixels in the output grid
            output_grid[0, start_index:j] = output_color
            
            # Move the main iterator past the block we just processed
            i = j
        else:
            # If the current pixel is not red, just move to the next one
            i += 1

    # Return the modified grid
    return output_grid