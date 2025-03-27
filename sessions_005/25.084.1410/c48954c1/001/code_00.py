"""
Construct a 9x9 grid by tiling transformed versions of a 3x3 input grid.
The tiling follows a specific pattern:
- The center tile is the original input grid.
- Tiles directly above and below the center are vertically flipped versions of the input.
- Tiles directly to the left and right of the center are horizontally flipped versions of the input.
- The four corner tiles are versions flipped both horizontally and vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a 9x9 output grid based on a tiling pattern
    of the original and flipped versions of the input.

    Args:
        input_grid (list of list of int): A 3x3 grid represented as a list of lists.

    Returns:
        list of list of int: The transformed 9x9 grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions (should be 3x3)
    rows, cols = input_array.shape
    
    # Create the transformed versions of the input grid
    # Original (center)
    original = input_array
    # Flipped horizontally (left-right)
    flipped_h = np.fliplr(original)
    # Flipped vertically (top-bottom)
    flipped_v = np.flipud(original)
    # Flipped both horizontally and vertically (180-degree rotation)
    flipped_hv = np.fliplr(flipped_v) # Or np.flipud(flipped_h)

    # Initialize the output grid (9x9)
    output_rows = rows * 3
    output_cols = cols * 3
    output_grid_np = np.zeros((output_rows, output_cols), dtype=int)

    # Place the transformed grids into the output grid according to the pattern
    # Top row of tiles
    output_grid_np[0:rows, 0:cols] = flipped_hv      # Top-left
    output_grid_np[0:rows, cols:cols*2] = flipped_v  # Top-center
    output_grid_np[0:rows, cols*2:cols*3] = flipped_hv # Top-right

    # Middle row of tiles
    output_grid_np[rows:rows*2, 0:cols] = flipped_h      # Middle-left
    output_grid_np[rows:rows*2, cols:cols*2] = original  # Center
    output_grid_np[rows:rows*2, cols*2:cols*3] = flipped_h # Middle-right

    # Bottom row of tiles
    output_grid_np[rows*2:rows*3, 0:cols] = flipped_hv      # Bottom-left
    output_grid_np[rows*2:rows*3, cols:cols*2] = flipped_v  # Bottom-center
    output_grid_np[rows*2:rows*3, cols*2:cols*3] = flipped_hv # Bottom-right

    # Convert the final numpy array back to a list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid