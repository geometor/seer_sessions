```python
"""
Identifies a primary structure defined by yellow (4) pixels and calculates its bounding box.
Finds trigger pixels (orange, 7) located outside this bounding box.
Based on the relative position of each trigger pixel (horizontal or vertical) to the bounding box,
fills the corresponding row or column with the trigger pixel color (orange, 7),
extending the fill from the trigger pixel's coordinate across the span of the bounding box on that axis.
The fill operation overwrites any pixel *unless* the original pixel in the input grid was the boundary color (yellow, 4).
"""

import numpy as np

def find_color_pixels(grid, color):
  """Finds all coordinates (row, col) of pixels with a specific color."""
  rows, cols = np.where(grid == color)
  return list(zip(rows, cols))

def get_bounding_box(coords):
  """
  Calculates the minimum bounding box (min_row, max_row, min_col, max_col)
  for a set of coordinates. Returns None for all values if coords is empty.
  The returned max values are inclusive.
  """
  if not coords:
    return None, None, None, None
  rows = [r for r, c in coords]
  cols = [c for r, c in coords]
  return min(rows), max(rows), min(cols), max(cols)

def transform(input_grid):
    """
    Applies the transformation rule based on trigger pixels outside a boundary's bounding box.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    boundary_color = 4
    trigger_color = 7

    # Find boundary pixels (yellow)
    boundary_coords = find_color_pixels(input_grid, boundary_color)

    # Calculate the bounding box of the boundary
    # If no boundary exists, return the original grid
    min_r, max_r, min_c, max_c = get_bounding_box(boundary_coords)
    if min_r is None:
        return output_grid

    # Find trigger pixels (orange)
    trigger_coords = find_color_pixels(input_grid, trigger_color)

    # Process each trigger pixel
    for tr, tc in trigger_coords:
        # Check if the trigger is outside the bounding box
        is_outside = (tr < min_r or tr > max_r or
                      tc < min_c or tc > max_c)

        if is_outside:
            # Determine if it's a horizontal or vertical trigger relative to the box
            # A trigger is horizontal if its row is within the box's row span,
            # but its column is outside the box's column span.
            is_horizontal_trigger = (min_r <= tr <= max_r) and \
                                    (tc < min_c or tc > max_c)
            # A trigger is vertical if its column is within the box's col span,
            # but its row is outside the box's row span.
            is_vertical_trigger = (min_c <= tc <= max_c) and \
                                  (tr < min_r or tr > max_r)

            # Apply fill for horizontal triggers
            if is_horizontal_trigger:
                # Determine the full column range to fill along the trigger row
                # This spans from the trigger column to the opposite side of the box
                start_c = min(tc, min_c)
                end_c = max(tc, max_c)
                # Iterate through the determined column range
                for c in range(start_c, end_c + 1):
                    # Check grid bounds just in case (though trigger row should be in bounds)
                    if 0 <= tr < height and 0 <= c < width:
                        # Check if the original pixel is NOT the boundary color
                        if input_grid[tr, c] != boundary_color:
                            # Change the pixel in the output grid
                            output_grid[tr, c] = trigger_color

            # Apply fill for vertical triggers
            elif is_vertical_trigger:
                # Determine the full row range to fill along the trigger column
                # This spans from the trigger row to the opposite side of the box
                start_r = min(tr, min_r)
                end_r = max(tr, max_r)
                # Iterate through the determined row range
                for r in range(start_r, end_r + 1):
                    # Check grid bounds just in case (though trigger col should be in bounds)
                    if 0 <= r < height and 0 <= tc < width:
                         # Check if the original pixel is NOT the boundary color
                        if input_grid[r, tc] != boundary_color:
                             # Change the pixel in the output grid
                            output_grid[r, tc] = trigger_color

    # Return the modified grid
    return output_grid
```