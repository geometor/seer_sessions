"""
Transforms the input grid by swapping pixel colors based on their initial values.
Pixels that are gray (5) in the input grid become the 'other' non-gray color 
present in the input grid. Pixels that have this 'other' color in the input 
grid become white (0).
"""

import numpy as np

def find_other_color(grid):
    """
    Finds the non-gray color in a grid assumed to contain only gray (5) 
    and one other color.
    
    Args:
        grid (np.array): The input grid.

    Returns:
        int: The value of the non-gray color, or None if only gray is present 
             or more than two colors exist (excluding gray).
    """
    unique_colors = np.unique(grid)
    other_color = None
    for color in unique_colors:
        if color != 5:
            # Found a non-gray color. Assuming only one such color exists.
            if other_color is None:
                 other_color = color
            else:
                # More than one non-gray color found, logic might be wrong for this case
                # Based on examples, we expect only one other color.
                # Let's return the first one found for now, or handle error?
                # Returning the first found aligns with the simple two-color swap idea.
                pass 
    return other_color

def transform(input_grid):
    """
    Applies the color swapping transformation to the input grid.
    
    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.
        
    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the grid.
    height, width = input_grid.shape

    # Identify the 'other' color (the non-gray color present).
    # Assumes exactly two colors: gray (5) and one other.
    other_color = find_other_color(input_grid)
    
    # Handle the edge case where no 'other_color' is found (e.g., grid is all gray)
    # Although examples suggest this won't happen. If it does, maybe return input?
    # For now, proceed assuming 'other_color' is found. If it's None, pixels won't match 
    # the second condition and gray pixels won't have a color to change to.
    # A safe default might be white(0) if other_color is None. Let's default to white.
    if other_color is None:
        # This case isn't in examples. If the grid was all gray, 
        # maybe the output should be all white? Or all the 'missing' other color?
        # Let's follow the logic: gray becomes other (which is undefined, maybe white?)
        # and other (non-existent) becomes white. Let's map gray to white in this case.
        other_color_replacement = 0 # Default replacement for gray if no other color found
    else:
        other_color_replacement = other_color

    # Initialize the output grid with the same shape, filled with a default value.
    # Using white (0) as a base seems reasonable since one transformation target is white.
    output_grid = np.zeros_like(input_grid)

    # Iterate through each pixel in the input grid.
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel.
            pixel_color = input_grid[r, c]

            # Apply the transformation rules:
            if pixel_color == 5:  # If the pixel is gray
                # Set the corresponding output pixel to the 'other' color
                output_grid[r, c] = other_color_replacement 
            elif pixel_color == other_color: # If the pixel is the 'other' color
                # Set the corresponding output pixel to white (0)
                output_grid[r, c] = 0
            # else:
                # If a pixel is neither gray nor the 'other' color (not expected from examples)
                # it currently remains 0 due to initialization. If preserving other colors
                # was needed, we'd copy input_grid first or handle it here.

    # Return the modified grid.
    return output_grid