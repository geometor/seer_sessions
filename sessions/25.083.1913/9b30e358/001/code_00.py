"""
1.  **Identify the Background:** Determine the most frequent color in the input grid, which represents the background.
2.  **Select Sub-region:** Locate the sub-region in the *lower half* of the input grid containing all the colors that are not the background color.
3. **Create a mirror:** Create a copy of the sub-region and mirror all rows vertically.
4.  **Overlay:** Overlay the mirrored region on top of the *upper half* of input, positioned at the input mirrored selection point.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    # Flatten the grid and count the occurrences of each color
    color_counts = Counter(grid.flatten())
    # Return the most common color (background color)
    return color_counts.most_common(1)[0][0]

def select_subregion(grid, background_color):
    rows, cols = grid.shape
    min_row, max_row = rows, 0
    min_col, max_col = cols, 0

    # Iterate through the lower half of the grid
    for r in range(rows // 2, rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                # Update boundaries of the sub-region
                min_row = min(min_row, r)
                max_row = max(max_row, r)
                min_col = min(min_col, c)
                max_col = max(max_col, c)

    # Adjust min_row to always maintain the selection in the bottom half, with
    # an offset.
    min_row = rows // 2
    return min_row, max_row, min_col, max_col

def mirror_subregion(grid, min_row, max_row, min_col, max_col):
    # Extract and vertically flip the selected sub-region
    subregion = grid[min_row:max_row+1, min_col:max_col+1]
    return np.flipud(subregion)

def transform(input_grid):
    input_grid = np.array(input_grid) # Ensure input is a numpy array
    output_grid = np.copy(input_grid) # Initialize output_grid as a copy of the input

    background_color = get_background_color(input_grid)  # Determine background color
    min_row, max_row, min_col, max_col = select_subregion(input_grid, background_color) # Find sub-region boundaries
    mirrored_region = mirror_subregion(input_grid, min_row, max_row, min_col, max_col)  # Mirror the selected sub-region

    # Overlay the mirrored region onto the upper half of the output grid
    rows, cols = input_grid.shape
    rows_mirrored = mirrored_region.shape[0]
    start_row_overlay = min_row - rows_mirrored # Calculate where to begin the overlay in the output grid

    output_grid[start_row_overlay:min_row, min_col:max_col+1] = mirrored_region

    return output_grid.tolist() # Return the transformed grid as a list