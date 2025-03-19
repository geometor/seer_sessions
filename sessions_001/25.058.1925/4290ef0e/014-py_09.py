"""
1.  **Examine Input:** Examine the input grid to determine the dimensions and pixel colors.

2.  **Identify Target Pixels:** Find all pixels that are *not* azure (color 8).

3. **Output Grid Creation:**
    *   **Case 1: All Azure:** If *all* pixels in the input grid are azure, create a 7x7 output grid filled entirely with azure (color 8).
    *   **Case 2: One Non-Azure Color, One or More Pixels**: If there is one and only one color other than azure and at least one pixel of that color exists, create a 7x7 black (color 0) output grid. Place a single pixel of the non-azure color in the bottom-right corner (position (6, 6)) of the output grid.
    *  **Case 3: Multiple target colors, small area**: If there are multiple non-azure colors present, and their bounding box fits within a 7x7 grid, create a 7x7 grid and position the non-azure pixels relative to the top-left corner of the bounding box on the input grid.
     *  **Case 4: Multiple target colors, large area**: If there are multiple non-azure colors, and the dimensions (height or width) of their bounding box is greater than 7, create a 7x7 black grid. Place one pixel with the color of the pixel farthest down and to the right on the bottom-right corner (position (6,6)) of the output grid.
    *   **Case 5: No pixels found.** If no target pixels are found, create a 7x7 output grid filled entirely with black (color 0).
"""

import numpy as np

def find_target_pixels(grid):
    """Finds all pixels that are not azure (color 8) and returns their coordinates and colors."""
    rows, cols = grid.shape
    target_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 8:
                target_pixels.append(((r, c), grid[r, c]))
    return target_pixels

def transform(input_grid):
    # Find target pixels (non-azure pixels).
    target_pixels = find_target_pixels(input_grid)

    # initialize output_grid
    output_grid = np.zeros((7, 7), dtype=int)

    # Case 1: All Azure
    if not target_pixels:
        if np.all(input_grid == 8):
          output_grid[:] = 8
        return output_grid

    # Case 2: One Non-Azure Color
    unique_colors = set(color for _, color in target_pixels)
    if len(unique_colors) == 1:
        output_grid[6, 6] = target_pixels[0][1]
        return output_grid

    # Case 3 & 4: Multiple target colors
    # get the coordinates of the target pixels
    coords = [coord for coord, _ in target_pixels]
    # calculate row and col min/max
    min_r = min(r for r, _ in coords)
    max_r = max(r for r, _ in coords)
    min_c = min(c for _, c in coords)
    max_c = max(c for _, c in coords)

    # calculate the size of the area to copy
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Case 3: if we can fit the identified rectangle, copy it
    if height <= 7 and width <=7:
        for (r,c), color in target_pixels:
            # shift the input to the output grid
            output_grid[r-min_r, c-min_c] = color
    else: # Case 4: fallback: find pixel farthest down and right
      # find bottom-right most pixel by sorting by row and then by column
      target_pixels.sort(key=lambda item: (item[0][0], item[0][1]), reverse=True)
      output_grid[6,6] = target_pixels[0][1]

    return output_grid