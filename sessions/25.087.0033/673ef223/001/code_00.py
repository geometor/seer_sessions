import numpy as np
import math

"""
Processes the input grid row by row to produce the output grid.

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each row of the input grid.
3.  For the current row, find the column indices of all red pixels (color 2) and all azure pixels (color 8).
4.  Check Conditions:
    *   If the row contains at least one red pixel and at least one azure pixel:
        *   For each azure pixel at column `c_azure`:
            *   Find the red pixel column `c_red` in the same row that has the minimum horizontal distance to `c_azure`.
            *   Determine the fill range:
                *   If `c_red < c_azure`, fill columns from `c_red + 1` up to (but not including) `c_azure`.
                *   If `c_red > c_azure`, fill columns from `c_azure + 1` up to (but not including) `c_red`.
            *   In the output grid's current row, set the color of the pixels in the determined fill range to azure (8).
            *   In the output grid's current row, set the color of the pixel at column `c_azure` to yellow (4).
    *   Else if the row contains at least one red pixel and no azure pixels:
        *   For every column `c` in the row:
            *   If the input pixel at `(row, c)` is not red (2), set the output pixel at `(row, c)` to azure (8).
    *   Else (the row contains no red pixels):
        *   The row remains unchanged.
5.  Return the modified output grid.
"""

def find_indices(row_array, color):
  """Finds the indices of a specific color in a 1D numpy array."""
  return np.where(row_array == color)[0]

def find_closest(target_index, indices_list):
  """Finds the index in indices_list closest to target_index."""
  if not len(indices_list):
    return -1 # Should not happen if called correctly based on logic
  
  min_dist = float('inf')
  closest_idx = -1
  
  for idx in indices_list:
    dist = abs(idx - target_index)
    if dist < min_dist:
      min_dist = dist
      closest_idx = idx
    # Tie-breaking: if distances are equal, prefer the one already found (no change needed)
    # Alternative tie-breaking could be implemented if needed (e.g., prefer left/right)
      
  return closest_idx

def transform(input_grid):
    """
    Applies the transformation rules based on red and azure pixels in each row.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Define colors
    red = 2
    azure = 8
    yellow = 4

    # Iterate through each row
    for r in range(height):
        current_row = input_np[r, :]
        
        # Find indices of red and azure pixels in the current row
        red_indices = find_indices(current_row, red)
        azure_indices = find_indices(current_row, azure)

        # Condition 1: Row contains both red and azure pixels
        if len(red_indices) > 0 and len(azure_indices) > 0:
            for c_azure in azure_indices:
                # Find the closest red pixel to this azure pixel
                c_red = find_closest(c_azure, red_indices)

                # Determine fill range and fill with azure
                if c_red < c_azure:
                    # Fill from red+1 up to azure
                    start_col = c_red + 1
                    end_col = c_azure
                    if start_col < end_col:
                       output_grid[r, start_col:end_col] = azure
                elif c_red > c_azure:
                    # Fill from azure+1 up to red
                    start_col = c_azure + 1
                    end_col = c_red
                    if start_col < end_col:
                        output_grid[r, start_col:end_col] = azure
                
                # Change the original azure pixel position to yellow
                output_grid[r, c_azure] = yellow

        # Condition 2: Row contains red pixels but no azure pixels
        elif len(red_indices) > 0 and len(azure_indices) == 0:
            # Fill all non-red pixels with azure
            for c in range(width):
                if input_np[r, c] != red:
                    output_grid[r, c] = azure

        # Condition 3: Row contains no red pixels (no action needed as output is a copy)
        # else:
        #     pass # Row remains unchanged

    # Convert back to list of lists if necessary, though numpy array is often fine
    return output_grid.tolist()