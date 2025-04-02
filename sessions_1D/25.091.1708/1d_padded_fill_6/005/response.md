```python
"""
Horizontally fill rows with color starting from the first non-background pixel.
Specifically, for each row, find the first (leftmost) pixel that is not white (0). 
If such a pixel is found, change all white (0) pixels located strictly to its right within the same row 
to the color of that first non-white pixel. Rows containing only white pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by filling white pixels to the right of the 
    first non-white pixel in each row with that non-white pixel's color.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation and copying
    # Create a copy to modify, leaving the original input unchanged
    output_grid = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the grid
    height, width = output_grid.shape

    # Iterate through each row of the grid
    for r in range(height):
        # Initialize variables for tracking the first non-white pixel (trigger) in the current row
        fill_color = None
        trigger_found = False

        # Iterate through each column (pixel) in the current row from left to right
        for c in range(width):
            # Get the color of the current pixel from the grid we are modifying
            current_color = output_grid[r, c]

            # Phase 1: Search for the first non-white pixel (trigger) in the row
            if not trigger_found:
                # Check if the current pixel is not the background color (white, 0)
                if current_color != 0:
                    # Found the trigger pixel
                    trigger_found = True
                    # Store its color to be used for filling
                    fill_color = current_color
                    # No modification needed for the trigger pixel itself, continue to the next pixel
                    continue 
            
            # Phase 2: Fill white pixels to the right once the trigger is found
            # This block executes only if trigger_found is True
            if trigger_found:
                # Check if the current pixel is white (0)
                if current_color == 0:
                    # Change this white pixel to the stored fill_color
                    output_grid[r, c] = fill_color
                # If the current pixel is non-white and to the right of the trigger, 
                # it remains unchanged (as per the problem description)

    # Convert the modified numpy array back to a list of lists for the return value
    return output_grid.tolist()
```