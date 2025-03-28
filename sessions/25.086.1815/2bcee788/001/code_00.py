"""
Transforms an input grid based on the following rules:
1.  Determine the height and width of the input grid.
2.  Scan the input grid to find the unique non-white (0) colors present. Identify the color that is *not* red (2); let this be the `fill_color`.
3.  Create a new output grid with the same height and width as the input grid.
4.  Initialize all cells of the output grid with the color green (3).
5.  Iterate through each cell of the input grid at `(row, column)`.
6.  If the color of the input cell at `(row, column)` is red (2) or the identified `fill_color`, set the color of the output grid cell at `(row, column)` to the `fill_color`.
7.  Return the completed output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid with integer color values.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # --- Step 2: Identify the non-red, non-background color ---
    unique_colors = np.unique(input_array)
    non_background_colors = unique_colors[unique_colors != 0] # Exclude white (0)
    
    fill_color = -1 # Initialize with an invalid value
    red_color = 2
    background_color_out = 3 # green

    if len(non_background_colors) == 0:
        # Handle case with only background color
        fill_color = background_color_out # Or handle as error/specific case if needed
    elif len(non_background_colors) == 1:
        # If only one non-background color, use it (even if it's red)
        fill_color = non_background_colors[0]
    else:
        # Find the color that is not red (2)
        for color in non_background_colors:
            if color != red_color:
                fill_color = color
                break
        # If fill_color wasn't found (e.g., only red and background present), default to red
        if fill_color == -1:
             fill_color = red_color


    # --- Step 3 & 4: Create and initialize the output grid ---
    # Initialize output grid with the background color (green, 3)
    output_grid = np.full((height, width), background_color_out, dtype=int)

    # --- Step 5 & 6: Iterate and replace pixels ---
    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            input_color = input_array[r, c]
            # Check if the input color is red (2) or the identified fill_color
            if input_color == red_color or input_color == fill_color:
                 # If the input pixel belongs to the object (either red or the other color)
                 # set the corresponding output pixel to the fill_color
                 output_grid[r, c] = fill_color

    # --- Step 7: Return the output grid ---
    return output_grid.tolist() # Return as list of lists if preferred, or keep as numpy array