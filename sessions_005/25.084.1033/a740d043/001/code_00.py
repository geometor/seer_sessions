"""
1. Determine the background color by finding the most frequent pixel value in the input grid.
2. Identify the coordinates of all pixels in the input grid whose color is *not* the background color.
3. Calculate the minimum row index (`min_row`), maximum row index (`max_row`), minimum column index (`min_col`), and maximum column index (`max_col`) among the coordinates identified in step 2. This defines the bounding box.
4. Create a new output grid with height (`max_row - min_row + 1`) and width (`max_col - min_col + 1`).
5. Iterate through each cell `(r, c)` within the bounding box in the input grid (from `min_row` to `max_row` and `min_col` to `max_col`).
6. Get the color `color_in` of the input grid cell `(r, c)`.
7. If `color_in` is the background color, set the corresponding cell `(r - min_row, c - min_col)` in the output grid to white (0).
8. Otherwise (if `color_in` is not the background color), set the corresponding cell `(r - min_row, c - min_col)` in the output grid to `color_in`.
9. Return the completed output grid.
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    if grid.size == 0:
        return 0 # Default or handle error as appropriate
    counts = Counter(grid.flatten())
    # Assuming background is the most frequent color
    background_color = counts.most_common(1)[0][0]
    return background_color

def transform(input_grid):
    """
    Extracts non-background objects within their minimal bounding box,
    replacing the background color within that box with white (0).
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    if input_np.size == 0:
        return [] # Handle empty input

    # Step 1: Identify the background color
    background_color = find_background_color(input_np)

    # Step 2: Locate all foreground pixels
    foreground_pixels = np.where(input_np != background_color)

    # Handle case where there are no foreground pixels
    if len(foreground_pixels[0]) == 0:
        # Or return based on specific task requirements if all pixels are background
        # For this task, based on examples, we expect foreground objects.
        # If truly no foreground, perhaps an empty grid or original is expected.
        # Returning empty seems plausible if the goal is object extraction.
        return [] # Or maybe [[0]]? Let's stick to empty for now.

    # Step 3: Determine the minimum bounding box
    min_row = np.min(foreground_pixels[0])
    max_row = np.max(foreground_pixels[0])
    min_col = np.min(foreground_pixels[1])
    max_col = np.max(foreground_pixels[1])

    # Step 4: Extract the subgrid defined by the bounding box
    subgrid = input_np[min_row:max_row+1, min_col:max_col+1]

    # Step 5 & 7 & 8: Create the output grid by replacing background color with white (0)
    # Create a copy to avoid modifying the original slice if needed elsewhere
    output_np = subgrid.copy()
    output_np[output_np == background_color] = 0

    # Step 9: Return the completed output grid (convert back to list of lists)
    output_grid = output_np.tolist()

    return output_grid