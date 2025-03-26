"""
Transforms an input grid by applying a fixed color substitution rule to each pixel independently. 
The rule is defined by a specific mapping:
1 -> 5
2 -> 6
3 -> 4
4 -> 3
5 -> 1
6 -> 2
8 -> 9
9 -> 8
Colors 0 and 7 are assumed to remain unchanged as they were not present in the training examples.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a fixed pixel-wise color substitution to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Define the color mapping based on the observed examples
    color_map = {
        1: 5,  # blue -> gray
        2: 6,  # red -> magenta
        3: 4,  # green -> yellow
        4: 3,  # yellow -> green
        5: 1,  # gray -> blue
        6: 2,  # magenta -> red
        8: 9,  # azure -> maroon
        9: 8   # maroon -> azure
        # Colors 0 and 7 are implicitly mapped to themselves if encountered
    }

    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid with the same dimensions, filled with zeros initially
    # Alternatively, copy the input grid to handle unchanged colors by default
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            input_color = input_grid[r, c]
            
            # Apply the color substitution using the map
            # Use .get(key, default_value) to handle colors not in the map
            # If input_color is in color_map, use its value; otherwise, use input_color itself
            output_color = color_map.get(input_color, input_color)
            
            # Assign the new color to the corresponding pixel in the output grid
            output_grid[r, c] = output_color

    # Return the transformed grid
    return output_grid