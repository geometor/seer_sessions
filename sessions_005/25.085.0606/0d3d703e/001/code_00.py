"""
Applies a fixed color substitution to each pixel independently based on its color value.

The substitution map is:
- Blue (1) <-> Gray (5)
- Red (2) <-> Magenta (6)
- Green (3) <-> Yellow (4)
- Azure (8) <-> Maroon (9)
- White (0) and Orange (7) remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by applying a fixed color substitution to each pixel.

    Args:
        input_grid (list[list[int]] or np.ndarray): A 2D grid of integer color values.

    Returns:
        np.ndarray: The transformed grid with substituted colors.
    """
    # Define the color substitution mapping
    color_map = {
        1: 5,  # Blue -> Gray
        5: 1,  # Gray -> Blue
        2: 6,  # Red -> Magenta
        6: 2,  # Magenta -> Red
        3: 4,  # Green -> Yellow
        4: 3,  # Yellow -> Green
        8: 9,  # Azure -> Maroon
        9: 8,  # Maroon -> Azure
        0: 0,  # White -> White (unchanged)
        7: 7   # Orange -> Orange (unchanged)
    }

    # Convert input to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    height, width = input_array.shape

    # Initialize the output grid with the same dimensions, copying the input initially
    # or creating a zero grid of the same size
    output_grid = np.zeros_like(input_array)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Get the color value of the current pixel
            input_color = input_array[r, c]
            
            # Determine the output color using the map
            # If the color is not explicitly in the map, it defaults to itself (handled by the map definition)
            output_color = color_map.get(input_color, input_color) # .get is robust, but map includes all 0-9 now
            
            # Set the corresponding pixel in the output grid
            output_grid[r, c] = output_color

    return output_grid.tolist() # Return as list of lists per ARC standard if needed, np array is often fine too.
                                # Let's stick to list of lists for consistency with problem description.