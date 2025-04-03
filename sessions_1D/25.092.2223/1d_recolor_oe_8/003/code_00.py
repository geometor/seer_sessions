import numpy as np

# Color constants
MAROON = 9
GREEN = 3
MAGENTA = 6
WHITE = 0

"""
Transforms a grid by changing the color of contiguous horizontal blocks of maroon (9) pixels within each row.
The transformation rule is applied independently to each row.
Within a row:
1. The first contiguous block of maroon (9) pixels encountered (reading from left to right) is changed to green (3).
2. All subsequent contiguous blocks of maroon (9) pixels in that same row are changed to magenta (6).
3. White (0) pixels remain unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the color transformation rule to the input grid.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(rows):
        # Flag to track if the first maroon block in this row has been processed
        first_maroon_block_processed_in_row = False
        # Variable to store the target color for the current block in this row
        current_block_target_color = -1 # Initialize with an invalid color
        # Flag to track if we are currently inside a maroon block in this row
        in_maroon_block = False

        # Iterate through each pixel (column) of the current row
        for c in range(cols):
            pixel = input_grid[r, c]

            if pixel == MAROON:
                # Check if this is the start of a new maroon block
                if not in_maroon_block:
                    in_maroon_block = True
                    # Determine the target color for this new block
                    if not first_maroon_block_processed_in_row:
                        current_block_target_color = GREEN
                        first_maroon_block_processed_in_row = True # Mark the first block in this row as processed
                    else:
                        current_block_target_color = MAGENTA
                
                # Apply the transformation for the current block to the output grid
                output_grid[r, c] = current_block_target_color
            
            else: # Pixel is not MAROON (must be WHITE based on examples)
                # If we were in a maroon block, we are now exiting it
                if in_maroon_block:
                    in_maroon_block = False
                # White pixels remain white (already copied during initialization)
                # output_grid[r, c] = WHITE # This line is redundant

    return output_grid