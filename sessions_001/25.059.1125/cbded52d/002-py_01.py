"""
The transformation rule is as follows:

1.  **Identify Marker Pixels:** Locate all pixels in the input grid that have a color value other than 0 (black) or 1 (blue). These are the "marker" pixels.
2.  **Copy Background:** All pixels that are value 0 (black) or 1 (blue) remain unchanged from the input to the output.
3.  **Transform Markers:** For each row containing marker pixels:
      a. Examine the first non 0 or 1 pixel in the row. Note this location.
      b. Output the noted value into the output grid at this same location.
      c. Note the value to the left of the first marker.
      d. Continue to shift this value to all non 0 or 1 marker locations in the row.
4.  **Copy Unchanged Rows:** All rows that *do not* contain any marker pixels are copied directly from the input to the output without modification.
"""

import numpy as np

def find_marker_pixels(grid):
    """Finds pixels that are not 0 or 1."""
    marker_pixels = []
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            if pixel != 0 and pixel != 1:
                marker_pixels.append((i, j, pixel))
    return marker_pixels

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    marker_pixels = find_marker_pixels(input_grid)

    # Group marker pixels by row
    marker_rows = {}
    for i, j, pixel in marker_pixels:
        if i not in marker_rows:
            marker_rows[i] = []
        marker_rows[i].append((i, j, pixel))

    # Transform markers in each row
    for row_index, markers in marker_rows.items():
        # Sort markers by column index
        markers.sort(key=lambda x: x[1])

        if markers:
           first_marker_row, first_marker_col, first_marker_val = markers[0]
           
           #get value to the left
           val_to_left = input_grid[first_marker_row, first_marker_col-1]
           #print(f"Val to left = {val_to_left}")

           for marker_row, marker_col, marker_val in markers:
               if (marker_col == first_marker_col):
                  output_grid[marker_row, marker_col] = first_marker_val
               else:
                  output_grid[marker_row, marker_col] = val_to_left

    return output_grid.tolist()