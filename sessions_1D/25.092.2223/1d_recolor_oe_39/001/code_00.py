"""
Color transformation based on object order.

This transformation operates on a 1D array of pixels.
It identifies contiguous segments (objects) of azure (color 8) pixels against a white (color 0) background.
The background pixels remain unchanged.
The first contiguous segment of azure pixels encountered when scanning from left to right is changed to blue (color 1).
All subsequent contiguous segments of azure pixels are changed to gray (color 5).
The length of the array and the positions of the segments are preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the described color transformation to the input grid.

    Args:
        input_grid (list or np.array): A 1D list or numpy array representing the input pixels.

    Returns:
        np.array: A 1D numpy array representing the transformed pixels.
    """
    # Ensure input is a numpy array
    # The input examples are given as single rows, so we expect a 1D array/list.
    # If the input is [[...]], take the first element. If it's [...], use it directly.
    if isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
         grid = np.array(input_grid[0], dtype=int)
    else:
         grid = np.array(input_grid, dtype=int)


    # Initialize output_grid as a copy of the input grid.
    # This handles preserving background (0) pixels automatically.
    output_grid = grid.copy()

    # Flag to track if the first azure object has been found and colored blue.
    first_object_found = False

    # Get the length of the grid
    n = len(grid)
    
    # Iterate through the grid using an index
    i = 0
    while i < n:
        # Check if the current pixel is azure (8)
        if grid[i] == 8:
            # Check if this is the start of a new azure object
            # It's the start if it's the first pixel (i=0) or the previous pixel was not azure (grid[i-1] != 8)
            # Since we skip processed objects, we only need to check if grid[i] == 8
            
            # Determine the target color for this object
            if not first_object_found:
                target_color = 1  # Blue for the first object
                first_object_found = True # Set the flag
            else:
                target_color = 5  # Gray for subsequent objects

            # Find the end of the current contiguous azure object
            start_index = i
            while i < n and grid[i] == 8:
                i += 1
            end_index = i # end_index is the first position *after* the object

            # Color the entire object in the output grid with the target color
            output_grid[start_index:end_index] = target_color
            
            # The loop variable 'i' is already updated to the position after the object,
            # so the loop will continue from the next pixel.
        else:
            # If the pixel is not azure (it must be white/background), just move to the next pixel.
            i += 1

    # Return the modified grid
    return output_grid.tolist() # Return as a list to match expected output format if necessary