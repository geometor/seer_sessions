"""
1.  **Create Output Grid:** Create an output grid with dimensions twice the height and twice the width of the input grid.

2.  **Replicate Input (2x2 Tiling):**  The output consists of four copies of a *transformed* version of the input grid, arranged in a 2x2 tile.

3.  **Transform Input (Within Each Tile):** Within *each* of the four regions (which will become tiles) in the output grid, a specific transformation of the input is applied. The transform of the input will be used to populate the tiles:
     - The top left pixel swaps with the top center pixel in example 1: 8<->5; Example 2: 3 <-> 8; example 3: 0 <->3
     - After these swaps, the rest of the pixels are placed in the grid to create a mirrored effect.

4. **Populate Tiles:** Each of the four regions must be populated with the transform.
"""

import numpy as np

def transform_tile(input_grid):
    """Transforms a single tile based on the observed pattern."""
    input_grid = np.array(input_grid)
    transformed_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Swap top-left and top-center pixels
    if width >= 2:  # Ensure there's a top-center pixel
      transformed_grid[0, 0], transformed_grid[0, 1] = transformed_grid[0, 1], transformed_grid[0, 0]

    # horizontal mirror of top row
    if width > 2:
      for w in range(2,width):
        transformed_grid[0,width-w] = input_grid[0,w]


    #Mirror along main diagonal after swap.
    for r in range(1,height):
      for c in range(width):
        transformed_grid[r,c] = input_grid[c,r] if c < width and r < height else input_grid[r,c]


    return transformed_grid

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # transform input
    transformed_input = transform_tile(input_grid)

    # replicate input into each region (2x2 tiling)
    for i in range(2):
        for j in range(2):
            output_grid[i * input_height:(i + 1) * input_height, j * input_width:(j + 1) * input_width] = transformed_input

    return output_grid