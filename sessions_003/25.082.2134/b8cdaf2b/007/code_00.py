"""
1.  **Identify the Bottom Object:** Find the contiguous horizontal line object along the bottom row of the input grid. If no such object is present, make no changes.
2.  **Determine the Mirroring Region:**
    *   Calculate the vertical center (column index) of the identified bottom object using the formula: `center = (min_col + max_col) / 2`, where `min_col` and `max_col` are the leftmost and rightmost column indices of the bottom object, respectively.
    *   Identify the row immediately above the bottom object. This is the source row for mirroring.
3.  **Mirror the Source Row Segment:**
    *   Within the source row, mirror the colors of the pixels across the calculated vertical center. The mirroring only affects the segment of the source row that lies directly above the bottom object.  Specifically, for each pixel in the source row segment, calculate its horizontal distance (`delta_c`) from the center. Copy the color of the pixel at `center + delta_c` to the pixel at `center - delta_c`, and vice versa, ensuring both positions are within the grid boundaries.
4.  **Propagate Upwards:**
    *  Identify a range of columns based on bottom object: `[min_col...max_col]`
    *  Copy the mirrored section of source row to higher rows.
    *  Working upwards from the source row to the top of the grid (row 0), replace only the pixels in range `[min_col...max_col]` with the corresponding pixels from the mirrored section of the source row.
"""

import numpy as np

def find_bottom_object(grid):
    """Finds the contiguous horizontal object at the bottom of the grid."""
    rows, cols = grid.shape
    bottom_row = rows - 1
    bottom_pixels = []

    # Find all pixels on the bottom row that are not white (0)
    for c in range(cols):
        if grid[bottom_row, c] != 0:
            bottom_pixels.append((bottom_row, c))

    # Check for contiguity and create the object
    if bottom_pixels:
        contiguous_object = []
        bottom_pixels.sort(key=lambda x: x[1])  # Sort by column
        current_col = bottom_pixels[0][1]
        contiguous_object.append(bottom_pixels[0])

        for i in range(1, len(bottom_pixels)):
            if bottom_pixels[i][1] == current_col + 1 and grid[bottom_pixels[i][0], bottom_pixels[i][1]] == grid[contiguous_object[-1][0], contiguous_object[-1][1]]:
                contiguous_object.append(bottom_pixels[i])
                current_col += 1
            else:
              if len(contiguous_object) > 1:
                return contiguous_object #return if more than one pixel
              else: #reset and keep looking
                contiguous_object = [bottom_pixels[i]]
                current_col = bottom_pixels[i][1]

        if len(contiguous_object) > 1:
          return contiguous_object
        else:
          return [] #return empty if not long enought

    return []

def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    
    #find bottom object
    bottom_object = find_bottom_object(grid)

    if not bottom_object:
        return output_grid.tolist()

    # find mirroring region
    min_col = min(c for _, c in bottom_object)
    max_col = max(c for _, c in bottom_object)
    center = (min_col + max_col) / 2
    source_row = bottom_object[0][0] - 1

    # mirror source row
    if source_row >= 0:
        for c in range(min_col, max_col + 1):
            delta_c = c - center
            target_c = int(center - delta_c)
            if min_col <= target_c <= max_col:
              output_grid[source_row, target_c] = grid[source_row, c]

    # propagate upwards
    for r in range(source_row - 1, -1, -1):
        output_grid[r, min_col:max_col+1] = output_grid[source_row, min_col:max_col+1]
        

    return output_grid.tolist()