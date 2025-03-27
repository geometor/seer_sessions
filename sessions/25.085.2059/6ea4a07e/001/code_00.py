"""
Transforms an input grid by swapping the single non-white color (C1) with white (0), 
and replacing the original white (0) pixels with a new color (C2). 
The mapping from C1 to C2 is: gray(5) -> yellow(4), azure(8) -> red(2), green(3) -> blue(1).
"""

import numpy as np

def find_non_white_color(grid):
  """Finds the unique non-white color in the grid."""
  unique_colors = np.unique(grid)
  for color in unique_colors:
    if color != 0:
      return color
  return None # Should not happen based on task description

def get_output_color(input_color):
  """Determines the output color C2 based on the input color C1."""
  mapping = {
      5: 4,  # gray -> yellow
      8: 2,  # azure -> red
      3: 1   # green -> blue
  }
  return mapping.get(input_color, 0) # Default to white if no mapping found, though not expected

def transform(input_grid):
    """
    Applies the color swap and replacement transformation.
    
    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    
    # Find the non-white input color (C1)
    c1 = find_non_white_color(input_array)
    if c1 is None:
        # Handle case where input grid is all white (though not seen in examples)
        return input_array # Or return an error/specific output? Returning input for now.

    # Determine the corresponding output color (C2)
    c2 = get_output_color(c1)

    # Initialize output_grid with the same shape as input, filled with zeros
    output_grid = np.zeros_like(input_array)

    # Iterate through each pixel and apply the transformation rule
    for r in range(input_array.shape[0]):
        for c in range(input_array.shape[1]):
            input_pixel_color = input_array[r, c]
            
            # If the input pixel is C1, make the output pixel white(0)
            if input_pixel_color == c1:
                output_grid[r, c] = 0
            # If the input pixel is white(0), make the output pixel C2
            elif input_pixel_color == 0:
                output_grid[r, c] = c2
            # Optional: Handle unexpected colors if necessary, though not seen in examples
            # else: 
            #    output_grid[r, c] = input_pixel_color # Keep unexpected colors unchanged?

    return output_grid.tolist() # Return as list of lists, consistent with ARC format