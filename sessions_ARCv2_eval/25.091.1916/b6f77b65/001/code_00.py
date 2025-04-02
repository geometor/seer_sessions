import numpy as np

"""
Transformation Rule:

1. Identify the control color `C` located at the top-left corner (0, 0) of the input grid.
2. Determine the shift vector `(delta_row, delta_col)` based on the control color `C` using a predefined mapping:
    - If `C` is 9 (maroon), `(delta_row, delta_col) = (0, 0)`.
    - If `C` is 4 (yellow), `(delta_row, delta_col) = (3, 0)`.
    - If `C` is 6 (magenta), `(delta_row, delta_col) = (2, -3)`.
    - If `C` is 7 (orange), `(delta_row, delta_col) = (5, 2)`.
3. Create an output grid of the same dimensions as the input grid, initialized with the background color (white, 0).
4. Copy the control color `C` from the input grid's (0, 0) position to the output grid's (0, 0) position.
5. Iterate through all cells `(row, col)` of the input grid, excluding the control cell (0, 0).
6. For each non-background cell, calculate its new position `(new_row, new_col)` by adding the shift vector: `new_row = row + delta_row`, `new_col = col + delta_col`.
7. If the calculated `(new_row, new_col)` is within the bounds of the grid, copy the color from the input grid at `(row, col)` to the output grid at `(new_row, new_col)`. Pixels shifted outside the grid are discarded.
8. Return the final output grid.
"""

def transform(input_grid):
    """
    Applies a translation to the input grid based on the color of the top-left pixel.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_np)

    # Identify control color and determine shift vector
    control_color = input_np[0, 0]
    
    shift_vector = (0, 0) # Default to no shift
    if control_color == 9: # maroon
        shift_vector = (0, 0)
    elif control_color == 4: # yellow
        shift_vector = (3, 0)
    elif control_color == 6: # magenta
        shift_vector = (2, -3)
    elif control_color == 7: # orange
        shift_vector = (5, 2)
    # Add other color mappings here if needed based on test cases
        
    delta_row, delta_col = shift_vector

    # Preserve the control pixel in the output
    output_grid[0, 0] = control_color

    # Iterate through the input grid, skipping the control pixel
    for r in range(height):
        for c in range(width):
            # Skip the control pixel itself
            if r == 0 and c == 0:
                continue

            # Get the color of the current pixel
            color = input_np[r, c]

            # Skip background pixels
            if color == 0:
                continue

            # Calculate the new position after applying the shift
            new_r = r + delta_row
            new_c = c + delta_col

            # Check if the new position is within the grid bounds
            if 0 <= new_r < height and 0 <= new_c < width:
                # Place the pixel at the new position in the output grid
                output_grid[new_r, new_c] = color
                
    # Convert back to list of lists for the required output format
    return output_grid.tolist()