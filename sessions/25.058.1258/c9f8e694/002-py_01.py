"""
The transformation rule is as follows:

1.  **Identify the Target Color:** In each pair, find the color that changes from input to output (5 in example one and 5 in example two).

2.  **Identify Seed color** Locate the seed color - color of the pixel directly left of Target color at top left corner of the grid. If left side is Target color or 0, then locate pixel directly above first instance.

3. **Replace target color pixels:** Replace the color in the target color pixels with the seed color.
4.  **Preserve Other Colors:** All other colors in the input grid remain unchanged in the output grid.
"""

import numpy as np

def find_target_color(input_grid, output_grid):
    # Identify the color that changes from the input to the output.
    input_flat = input_grid.flatten()
    output_flat = output_grid.flatten()
    
    for i in range(len(input_flat)):
        if input_flat[i] != output_flat[i]:
            return input_flat[i]
    return None  # No color changed

def find_seed_color(input_grid, target_color):
    # Find the seed color, which is the color to the left of the top-left target color pixel.
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == target_color:
                if c > 0 and input_grid[r,c-1] != 0 and input_grid[r, c-1] != target_color:
                    return input_grid[r, c - 1]
                elif r>0 and input_grid[r-1,c] != 0 and input_grid[r-1,c] != target_color:
                    return input_grid[r-1,c]
    return None

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Initialize output as copy to preserve other colours.

    # dummy output_grid for target finding
    dummy_output = np.zeros_like(input_grid)

    rows, cols = input_grid.shape

    # dummy grid to find change
    for r in range(rows):
        for c in range(cols):
          if(input_grid[r,c] != 0):
            dummy_output[r,c] = 1
            

    target_color = find_target_color(input_grid, dummy_output)
    if target_color is None:
        return output_grid.tolist()  # No change, return original

    seed_color = find_seed_color(input_grid, target_color)
    if seed_color is None:
      return output_grid.tolist() # no seed

    # change all target colors
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == target_color:
                output_grid[r, c] = seed_color

    return output_grid.tolist()