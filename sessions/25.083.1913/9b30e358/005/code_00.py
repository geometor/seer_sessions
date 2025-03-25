"""
1.  **Identify Background:** Determine the most frequent color in the input grid. This is the background color.

2.  **Select Sub-region:** In the lower half of the input grid, identify the smallest rectangular region (bounding box) that contains all pixels that *are not* the background color.

3.  **Mirror Sub-region:** Create a vertically flipped (mirrored) copy of the selected sub-region.

4.  **Overlay Mirrored Region:** Copy the mirrored region on the top of a new grid, starting at the first row (row 0). Use the column positions from the bounding box of the original non-background sub-region, *do not* offset the overlay.

5. **Copy the original grid:** The final output is the original grid with the mirrored region overlaid on top of it.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    """Finds the most frequent color in a grid."""
    color_counts = Counter(grid.flatten())
    return color_counts.most_common(1)[0][0]

def select_subregion(grid, background_color):
    """Finds the bounding box of non-background pixels in the lower half."""
    rows, cols = grid.shape
    min_row, max_row = rows, 0  # Initialize min_row to a large value, max_row to 0
    min_col, max_col = cols, 0  # Initialize min_col to a large value, max_col to 0

    for r in range(rows // 2, rows):  # Iterate only through the lower half
        for c in range(cols):
            if grid[r, c] != background_color:
                min_row = min(min_row, r)  # Update min_row if a smaller row is found
                max_row = max(max_row, r)  # Update max_row if a larger row is found
                min_col = min(min_col, c)  # Update min_col if a smaller column is found
                max_col = max(max_col, c)  # Update max_col if a larger column is found

    # Handle the edge case where there are no non-background pixels.
    if max_row < rows //2: #no non-background object found
        return None

    return min_row, max_row, min_col, max_col

def mirror_subregion(grid, subregion_coords):
    """Vertically flips the selected sub-region."""
    min_row, max_row, min_col, max_col = subregion_coords
    subregion = grid[min_row:max_row+1, min_col:max_col+1]
    return np.flipud(subregion)

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Identify the background color
    background_color = get_background_color(input_grid)

    # Select the sub-region in the lower half
    subregion_coords = select_subregion(input_grid, background_color)

    # Handle cases where there's no non-background object
    if subregion_coords is None:
        return output_grid.tolist()

    # Create a mirrored copy of the sub-region
    mirrored_region = mirror_subregion(input_grid, subregion_coords)

    # Overlay the mirrored region onto the top of the output grid
    min_row, max_row, min_col, max_col = subregion_coords
    rows_mirrored = mirrored_region.shape[0]
    output_grid[0:rows_mirrored, min_col:max_col+1] = mirrored_region

    return output_grid.tolist()