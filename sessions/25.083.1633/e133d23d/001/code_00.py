"""
1.  **Initialization:** Create an output grid identical in dimensions to the input grid.
2.  **Direct Mapping**: For every pixel in input, if the color is '4' change it to '2' in output.
3. **Color Substitution Based on Horizontal Neighbors**
    * For each '6'(magenta) in input, if directly left of a '4'(yellow) then convert to '2'(red).
    * For each '6'(magenta) in input, if directly right of a '4'(yellow) then convert to '2'(red).
4.  **Copy Unchanged Pixels**: All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid)  # Initialize output as a copy

    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Direct Mapping: If the cell is '4', change it to '2'
            if input_grid[r, c] == 4:
                output_grid[r, c] = 2
            # Horizontal Neighbor Check for '6'
            elif input_grid[r, c] == 6:
                # Check left neighbor
                if c > 0 and input_grid[r, c-1] == 4:
                    output_grid[r, c] = 2
                # Check right neighbor
                elif c < cols - 1 and input_grid[r, c+1] == 4:
                    output_grid[r, c] = 2

    return output_grid