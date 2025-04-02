"""
Transforms an input grid based on the following rules:
1. Creates a new output grid of the same dimensions as the input, filled with white (0).
2. Identifies all unique colors in the input grid, excluding white (0) and gray (5).
3. For each identified unique color:
    a. Finds all pixels in the input grid with this color and counts them.
    b. If the count is exactly 2:
        i. Determines the minimum row (min_r) and minimum column (min_c) of the bounding box containing these two pixels.
        ii. Applies a fixed 6-pixel pattern relative to (min_r, min_c) to the output grid using the current color. The relative coordinates are (0,0), (0,2), (1,1), (2,0), (2,1), (2,2). Pixels outside grid bounds are ignored.
    c. If the count is 1 or greater than 2:
        i. Determines the bounding box (min_r, max_r, min_c, max_c) for all pixels of this color.
        ii. Fills this bounding box rectangle in the output grid with the current color.
4. Returns the final output grid. Gray pixels (color 5) in the input are ignored.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the conditional pattern/bounding box transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get input grid dimensions
    height, width = input_grid.shape

    # 1. Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # 2. Find unique colors in the input grid, excluding white (0) and gray (5)
    unique_colors = np.unique(input_grid)
    colors_to_process = [c for c in unique_colors if c != 0 and c != 5]

    # 3. Process each relevant color
    for color in colors_to_process:
        # 3a. Find coordinates and count pixels of the current color
        rows, cols = np.where(input_grid == color)
        coords = list(zip(rows, cols))
        pixel_count = len(coords)

        # Skip if no pixels of this color are found (shouldn't happen with np.unique, but good practice)
        if pixel_count == 0:
            continue

        # 3b. Apply transformation if count is exactly 2
        if pixel_count == 2:
            # i. Find the top-left corner (min_row, min_col) of the bounding box
            min_r = np.min(rows)
            min_c = np.min(cols)

            # ii. Define the relative coordinates of the 6-pixel pattern
            pattern_relative_coords = [
                (0, 0), (0, 2),
                (1, 1),
                (2, 0), (2, 1), (2, 2)
            ]

            # Place the pattern pixels in the output grid, checking bounds
            for dr, dc in pattern_relative_coords:
                nr, nc = min_r + dr, min_c + dc
                if 0 <= nr < height and 0 <= nc < width:
                    output_grid[nr, nc] = color

        # 3c. Apply transformation if count is 1 or > 2
        else:
            # i. Calculate the bounding box
            min_r = np.min(rows)
            max_r = np.max(rows)
            min_c = np.min(cols)
            max_c = np.max(cols)

            # ii. Fill the bounding box area in the output grid
            # Slicing is [inclusive_start:exclusive_end], so add 1 to max indices
            output_grid[min_r : max_r + 1, min_c : max_c + 1] = color

    # 4. Return the final output grid
    return output_grid
