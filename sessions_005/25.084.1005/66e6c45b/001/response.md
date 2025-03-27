```python
"""
Transforms an input grid by finding a 2x2 block of non-white pixels and mapping 
these four pixels to the four corners of the output grid. The rest of the output 
grid is filled with the background color (white, 0).
"""

import numpy as np

def find_2x2_block(grid):
    """
    Finds the top-left coordinate of the first 2x2 block where all pixels are non-zero.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: The (row, col) of the top-left corner of the block, or None if not found.
    """
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if all four pixels in the 2x2 block are non-zero
            if (grid[r, c] != 0 and
                grid[r, c+1] != 0 and
                grid[r+1, c] != 0 and
                grid[r+1, c+1] != 0):
                return (r, c)
    return None # No such block found

def transform(input_grid):
    """
    Finds a 2x2 non-background block in the input and places its pixels
    at the corners of the output grid.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid with background color (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Find the 2x2 block of non-white pixels
    block_coords = find_2x2_block(input_np)

    if block_coords:
        r, c = block_coords
        
        # Extract the colors from the found block in the input grid
        top_left_color = input_np[r, c]
        top_right_color = input_np[r, c + 1]
        bottom_left_color = input_np[r + 1, c]
        bottom_right_color = input_np[r + 1, c + 1]

        # Place the extracted colors into the corners of the output grid
        output_grid[0, 0] = top_left_color          # Top-left corner
        output_grid[0, width - 1] = top_right_color # Top-right corner
        output_grid[height - 1, 0] = bottom_left_color # Bottom-left corner
        output_grid[height - 1, width - 1] = bottom_right_color # Bottom-right corner

    return output_grid.tolist() # Return as list of lists per specification

```