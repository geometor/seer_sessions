import numpy as np

"""
Transforms the input grid based on the color of the top-left pixel (0,0).

1.  Initialize an output grid of the same dimensions as the input, filled with white (0).
2.  Read the color `C` of the pixel at the top-left corner `(0,0)` of the input grid.
3.  Determine the vertical shift `dy` and horizontal shift `dx` based on `C`:
    - If `C` is 9 (maroon), `dy = 0`, `dx = 0`.
    - If `C` is 4 (yellow), `dy = 3`, `dx = 1`.
    - If `C` is 6 (magenta), `dy = 2`, `dx = 2`.
    - If `C` is 7 (orange), `dy = 5`, `dx = 3`.
    - Otherwise, assume no shift (`dy = 0`, `dx = 0`), although examples only cover these cases.
4.  Copy the color `C` from `input_grid[0,0]` to `output_grid[0,0]`.
5.  Iterate through each pixel `(r, c)` of the input grid, excluding the top-left pixel `(0,0)`.
6.  If the input pixel `input_grid[r, c]` is not white (0):
    a. Calculate the target coordinates: `new_row = r + dy`, `new_col = c + dx`.
    b. Check if the target coordinates `(new_row, new_col)` are within the grid boundaries.
    c. If within bounds, set `output_grid[new_row, new_col]` to the color `input_grid[r, c]`.
7. Return the final output grid.
"""

def transform(input_grid):
    """
    Applies a shift transformation to the non-background pixels of the input grid,
    determined by the color of the top-left pixel.

    Args:
        input_grid (list of lists): A 2D list of integers representing the input grid.

    Returns:
        list of lists: A 2D list of integers representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with white (0)
    output_array = np.zeros_like(input_array)

    # Read the indicator color from the top-left corner
    indicator_color = input_array[0, 0]

    # Determine the shift based on the indicator color
    dy, dx = 0, 0
    if indicator_color == 9: # maroon
        dy, dx = 0, 0
    elif indicator_color == 4: # yellow
        dy, dx = 3, 1
    elif indicator_color == 6: # magenta
        dy, dx = 2, 2
    elif indicator_color == 7: # orange
        dy, dx = 5, 3
    # No other indicator colors are present in the training examples.
    # If an unknown color appears, default shift is (0,0).

    # Copy the indicator pixel to the output
    output_array[0, 0] = indicator_color

    # Iterate through the input grid, skipping the indicator pixel (0,0)
    for r in range(height):
        for c in range(width):
            # Skip the top-left corner pixel as it's handled separately
            if r == 0 and c == 0:
                continue

            pixel_color = input_array[r, c]

            # If the pixel is not background (white)
            if pixel_color != 0:
                # Calculate the new coordinates after shifting
                new_r = r + dy
                new_c = c + dx

                # Check if the new coordinates are within the grid bounds
                if 0 <= new_r < height and 0 <= new_c < width:
                    # Place the pixel color in the new location in the output grid
                    output_array[new_r, new_c] = pixel_color

    # Convert the numpy array back to a list of lists for the expected output format
    return output_array.tolist()