"""
1.  **Iterate through each row of the input grid.**
2.  **Check for Blue Pixels:** For each row, determine if there are at least two blue pixels.
3.  **Conditional Transformation:**
    *   If a row contains *at least two* blue pixels, find the indices of the first (leftmost) and last (rightmost) blue pixels.
    *   Change all white pixels located *between* these two blue pixels to magenta.
4.  **No Change Condition:** If a row has fewer than two blue pixels, it remains unchanged.
5. **Output is the transformed grid.**
"""

import numpy as np

def find_outermost_blue_pixels(row):
    """Finds the indices of the first and last blue pixels in a row."""
    blue_indices = np.where(row == 1)[0]
    if len(blue_indices) >= 2:
        return blue_indices[0], blue_indices[-1]
    return None, None

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    rows, _ = input_grid.shape

    for r in range(rows):
        # Check for Blue Pixels and find outermost
        first_blue, last_blue = find_outermost_blue_pixels(output_grid[r])

        # Conditional Transformation
        if first_blue is not None and last_blue is not None:
            # Change white pixels between blue pixels to magenta
            for c in range(first_blue + 1, last_blue):
                if output_grid[r, c] == 0:
                    output_grid[r, c] = 6

    return output_grid