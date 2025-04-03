import numpy as np
from typing import List

# Color constants
MAROON = 9
GREEN = 3
MAGENTA = 6
WHITE = 0

"""
Transforms a 1D grid (represented as a list) based on contiguous blocks of maroon (9) pixels.

1. Iterates through the input grid from left to right.
2. Identifies contiguous horizontal blocks of maroon (9) pixels.
3. The first block of maroon pixels encountered is transformed entirely into green (3) pixels.
4. All subsequent blocks of maroon pixels are transformed entirely into magenta (6) pixels.
5. White (0) pixels remain unchanged.
"""

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the color transformation rule to the input grid.

    Args:
        input_grid: A list of integers representing the input grid row.

    Returns:
        A list of integers representing the transformed output grid row.
    """
    
    # Initialize the output grid as a copy of the input
    output_grid = list(input_grid)
    n = len(output_grid)
    
    # Flag to track if the first maroon block has been processed
    first_maroon_block_processed = False
    # Variable to store the target color for the current block
    current_block_target_color = -1 # Initialize with an invalid color
    # Flag to track if we are currently inside a maroon block
    in_maroon_block = False

    # Iterate through each pixel of the input grid
    for i in range(n):
        pixel = input_grid[i]

        if pixel == MAROON:
            # Check if this is the start of a new maroon block
            if not in_maroon_block:
                in_maroon_block = True
                # Determine the target color for this new block
                if not first_maroon_block_processed:
                    current_block_target_color = GREEN
                    first_maroon_block_processed = True # Mark the first block as processed
                else:
                    current_block_target_color = MAGENTA
            
            # Apply the transformation for the current block
            output_grid[i] = current_block_target_color
        
        else: # Pixel is not MAROON (must be WHITE based on examples)
            # If we were in a maroon block, we are now exiting it
            if in_maroon_block:
                in_maroon_block = False
            # White pixels remain white (already copied during initialization)
            # output_grid[i] = WHITE # This line is redundant as we initialize output_grid from input_grid
            pass 

    return output_grid