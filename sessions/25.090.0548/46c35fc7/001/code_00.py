"""
Identify all 3x3 subgrids within the input grid whose four corner cells (top-left, top-right, bottom-left, bottom-right) are not the background color orange (7). Rotate each of these identified 3x3 subgrids 90 degrees counter-clockwise in place. Pixels outside these rotated blocks remain unchanged.
"""

import numpy as np

def rotate_subgrid_counter_clockwise(subgrid):
  """
  Rotates a 3x3 numpy array 90 degrees counter-clockwise.
  """
  # np.rot90 rotates counter-clockwise by default
  return np.rot90(subgrid, k=1)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    height, width = input_np.shape
    background_color = 7
    subgrid_size = 3

    # Iterate through all possible top-left corners (r, c) for a 3x3 subgrid
    # The range ensures that the 3x3 subgrid fits entirely within the grid boundaries
    for r in range(height - subgrid_size + 1):
        for c in range(width - subgrid_size + 1):
            
            # Define the coordinates of the four corners of the current 3x3 subgrid
            top_left = (r, c)
            top_right = (r, c + subgrid_size - 1)
            bottom_left = (r + subgrid_size - 1, c)
            bottom_right = (r + subgrid_size - 1, c + subgrid_size - 1)

            # Check if none of the four corner pixels have the background color (7)
            if (input_np[top_left] != background_color and
                input_np[top_right] != background_color and
                input_np[bottom_left] != background_color and
                input_np[bottom_right] != background_color):

                # Extract the 3x3 subgrid from the input grid
                subgrid_to_rotate = input_np[r:r + subgrid_size, c:c + subgrid_size]
                
                # Perform a 90-degree counter-clockwise rotation
                rotated_subgrid = rotate_subgrid_counter_clockwise(subgrid_to_rotate)
                
                # Place the rotated 3x3 block into the output grid at the same position
                output_grid[r:r + subgrid_size, c:c + subgrid_size] = rotated_subgrid

    # Return the modified output grid
    return output_grid.tolist() # Return as list of lists if required by caller context
