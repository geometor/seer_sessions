"""
1. **Examine the input grid:** Determine its dimensions (height and width).
2.  **Find Blue Stripe:** Scan the input grid to identify a vertical stripe of blue pixels (color 1). Note the column index of this stripe. If no blue stripe is found, the column index is -1.
3.  **Create Output Grid:** Create an output grid with the same height as the input grid and a fixed width of 3. Initialize all cells to white (color 0).
4.  **Conditional Green "L's":**
    *   If a blue stripe *was* found AND the input grid height is greater than 2:
        *   Place an "L" shaped green object (color 3) in the top left of the output grid, such that its corner is at row 1, column 0.
        *   Place a *mirrored* "L" shaped green object in the bottom right of the output grid. The vertical arm should on on the last row and the second to last row and the horizontal arm should extend to the left.
    *   If no blue stripe was found, no other actions are to be performed
    * If a blue stripe was found AND the input grid height is 2:
        * Place a *mirrored* "L" shaped green object in the bottom right of the output grid.
5.  **Return Output Grid:** The output grid is the result of the transformation.
"""

import numpy as np

def find_vertical_stripe(grid, color):
    # Find the column index of the vertical stripe of the specified color
    height = grid.shape[0]
    for col in range(grid.shape[1]):
        if all(grid[row, col] == color for row in range(height)):
            return col
    return -1  # Return -1 if no such stripe is found

def transform(input_grid):
    # Find the column index of the blue vertical stripe (color 1)
    blue_stripe_col = find_vertical_stripe(input_grid, 1)

    # Initialize the output grid with all white pixels (color 0)
    output_height = input_grid.shape[0]
    output_width = 3
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # if no blue stripe is found, just return a blank grid
    if (blue_stripe_col == -1):
        return output_grid

    # Populate the output grid based on the blue stripe's position and height constraints
    if output_height > 2:
        # Place "L" at top left
        output_grid[1, 0] = 3
        output_grid[0, 1] = 3
        
        #Place mirrored "L" at bottom right
        output_grid[output_height - 2, 0] = 3
        output_grid[output_height - 1, 2] = 3

    elif output_height == 2:
        # Place mirrored "L" at bottom right
        output_grid[output_height - 2, 0] = 3
        output_grid[output_height - 1, 2] = 3
    elif output_height == 1:
        #do nothing since there is not enough room
        pass

    return output_grid