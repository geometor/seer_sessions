"""
1.  Identify Target Pixels: Examine the input grid and identify all pixels that are not azure (color 8).
2. Create Output Grid: If there is one and only one non-azure color, create a 7x7 output grid filled with black (color 0) and place the single pixel of the found color in the bottom right corner.
3. Handle Multiple Target Colors**: If there are multiple non-azure pixel colors, the program should determine their locations relative to each other, and re-create that relative positioning and color in the output grid, with black (color 0) used for empty cells. If it would overflow the 7x7 grid, then fallback to placing the pixel that is farthest down and to the right, and fill the output grid according to instruction 2.
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


    # If only one target pixel color, place it in the bottom-right corner.
    if len(set(color for _, color in target_pixels)) == 1:
      if len(target_pixels) > 0:
        output_grid[6, 6] = target_pixels[0][1]

    # handle more than one target pixel color
    elif len(target_pixels) > 1:
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

        # if we can fit the identified rectangle, copy it
        if height <= 7 and width <=7:
            for (r,c), color in target_pixels:
                # shift the input to the output grid
                output_grid[r-min_r, c-min_c] = color
        else: # fallback: find pixel farthest down and right
          # find bottom-right most pixel by sorting by row and then by column
          target_pixels.sort(key=lambda item: (item[0][0], item[0][1]), reverse=True)
          output_grid[6,6] = target_pixels[0][1]

    return output_grid