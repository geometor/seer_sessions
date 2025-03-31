```python
import numpy as np

"""
Transforms an input grid based on the following rules:
1. Initialize the output grid as a copy of the input grid.
2. Iterate through each pixel of the input grid.
3. If a pixel is white (0), check if there is an orange (7) pixel anywhere to its left AND anywhere to its right within the same row. If both conditions are met, change the corresponding pixel in the output grid to azure (8).
4. If a pixel is maroon (9), check if the pixel immediately to its left AND the pixel immediately to its right within the same row are both orange (7). If both conditions are met, change the corresponding pixel in the output grid to azure (8).
5. Otherwise, the pixel in the output grid retains its original color from the input grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_array)
    height, width = input_array.shape

    # Iterate through each row
    for r in range(height):
        # Find the column indices of all orange pixels in the current row
        orange_cols = [c for c in range(width) if input_array[r, c] == 7]

        # If there are no orange pixels or only one, no filling can happen in this row
        if len(orange_cols) < 2:
            continue

        # Iterate through each column in the current row
        for c in range(width):
            pixel_color = input_array[r, c]

            # Rule for white pixels (0)
            if pixel_color == 0:
                # Check for an orange pixel to the left
                has_left_orange = any(oc < c for oc in orange_cols)
                # Check for an orange pixel to the right
                has_right_orange = any(oc > c for oc in orange_cols)
                # If bounded by orange on both sides (any distance)
                if has_left_orange and has_right_orange:
                    output_grid[r, c] = 8  # Change to azure

            # Rule for maroon pixels (9)
            elif pixel_color == 9:
                # Check immediate left neighbor exists and is orange
                is_left_orange = (c > 0 and input_array[r, c - 1] == 7)
                # Check immediate right neighbor exists and is orange
                is_right_orange = (c < width - 1 and input_array[r, c + 1] == 7)
                # If immediately adjacent to orange on both sides
                if is_left_orange and is_right_orange:
                    output_grid[r, c] = 8  # Change to azure

            # Otherwise, the pixel retains its original color (already copied)

    return output_grid.tolist() # return as list of lists per spec

```