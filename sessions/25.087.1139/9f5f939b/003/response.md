```python
"""
Transformation Rule:
Iterate through each pixel of the input grid. If a pixel is azure (8), check two conditions:
1. Adjacency Check: All four pixels immediately adjacent cardinally (up, down, left, right) must be within the grid boundaries AND must also be azure (8).
2. Marker Check: All four pixels exactly two steps away cardinally (up, down, left, right) must be within the grid boundaries AND must be blue (1).
If both the Adjacency Check and the Marker Check are true for an azure pixel, change its color to yellow (4) in the output grid. Otherwise, the pixel retains its original color.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the refined transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for easier indexing and boundary checks
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Define the relevant colors
    target_color = 8      # Azure - the pixel we are checking
    adjacent_color = 8    # Azure - required color for adjacent pixels
    marker_color = 1        # Blue - required color for marker pixels at distance 2
    replacement_color = 4 # Yellow - the color to change the target pixel to

    # Define the relative positions for checks
    # Distance 1 (adjacent) cardinal offsets
    adjacent_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Distance 2 cardinal offsets
    marker_offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is the target color (azure)
            if input_array[r, c] == target_color:

                # Assume both conditions are met initially
                all_adjacents_ok = True
                all_markers_ok = True

                # --- Condition 1: Check Adjacent Pixels ---
                for dr, dc in adjacent_offsets:
                    nr, nc = r + dr, c + dc # Calculate adjacent neighbor coordinates

                    # Check if neighbor is out of bounds OR not the required adjacent color
                    if not (0 <= nr < height and 0 <= nc < width and input_array[nr, nc] == adjacent_color):
                        all_adjacents_ok = False
                        break # No need to check further adjacent pixels if one fails

                # --- Condition 2: Check Marker Pixels (only if adjacents were okay) ---
                if all_adjacents_ok: # Optimization: only check markers if adjacents passed
                    for dr, dc in marker_offsets:
                        nr, nc = r + dr, c + dc # Calculate marker neighbor coordinates

                        # Check if marker neighbor is out of bounds OR not the required marker color
                        if not (0 <= nr < height and 0 <= nc < width and input_array[nr, nc] == marker_color):
                            all_markers_ok = False
                            break # No need to check further marker pixels if one fails
                else:
                    # If adjacents failed, markers condition automatically fails for the change
                    all_markers_ok = False 

                # --- Update Output Grid ---
                # If both conditions (adjacent and marker checks) are met
                if all_adjacents_ok and all_markers_ok:
                    # Change the color of the pixel in the output grid to yellow
                    output_array[r, c] = replacement_color

    # Convert the NumPy array back to a list of lists for the final output
    return output_array.tolist()
```