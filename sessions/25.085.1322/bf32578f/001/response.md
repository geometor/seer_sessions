```python
"""
Transforms an input grid by identifying non-background pixels, calculating their bounding box and centroid, 
and drawing a modified rectangle in the output grid.

1. Find all non-background (non-zero) pixels in the input grid. Record their color and coordinates.
2. If no non-background pixels are found, return an output grid of the same dimensions filled with the background color (0).
3. Calculate the bounding box (min_row, max_row, min_col, max_col) of these pixels.
4. Calculate the average column index (centroid's column) of these pixels.
5. Calculate the center column index of the bounding box: (min_col + max_col) / 2.
6. Determine an offset: 1 if the average column index is strictly greater than the bounding box center column index, 0 otherwise.
7. Calculate the output rectangle's dimensions:
   - height = (bounding box height) - 2
   - width = (bounding box width) + 1
8. Calculate the output rectangle's top-left corner:
   - row = min_row + 1
   - column = floor(bounding box center column index) + offset
9. Create an output grid of the same dimensions as the input, filled with the background color (0).
10. Fill the calculated rectangular area in the output grid with the color of the non-background pixels found in step 1.
"""

import numpy as np
import math

def find_colored_pixels(grid):
    """Finds coordinates and the color of non-background pixels."""
    pixels = []
    color = None
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                pixels.append((r, c))
                if color is None:
                    color = grid[r, c]
                elif color != grid[r, c]:
                    # Assuming only one non-background color per task based on examples
                    pass 
    return pixels, color

def calculate_bounding_box(pixels):
    """Calculates the bounding box of a list of pixel coordinates."""
    if not pixels:
        return None
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output_grid with background color
    output_grid = np.zeros_like(input_array)

    # 1. Find all non-background pixels and their color
    pixels, color = find_colored_pixels(input_array)

    # 2. Handle case with no non-background pixels
    if not pixels:
        return output_grid.tolist()

    # 3. Calculate the bounding box
    min_row, max_row, min_col, max_col = calculate_bounding_box(pixels)
    bbox_height = max_row - min_row + 1
    bbox_width = max_col - min_col + 1

    # 4. Calculate the average column index (centroid column)
    avg_col_index = sum(c for r, c in pixels) / len(pixels)

    # 5. Calculate the center column index of the bounding box
    center_col_index = (min_col + max_col) / 2.0

    # 6. Determine the offset
    offset = 1 if avg_col_index > center_col_index else 0

    # 7. Calculate the output rectangle's dimensions
    out_height = bbox_height - 2
    out_width = bbox_width + 1

    # Check for non-positive dimensions, although unlikely based on examples
    if out_height <= 0 or out_width <= 0:
         return output_grid.tolist() # Draw nothing if dimensions invalid

    # 8. Calculate the output rectangle's top-left corner
    out_min_row = min_row + 1
    # Use math.floor for the integer part of the center column index
    out_min_col = math.floor(center_col_index) + offset

    # 9. Calculate output bottom-right corner (for slicing)
    out_max_row = out_min_row + out_height -1
    out_max_col = out_min_col + out_width - 1

    # 10. Fill the calculated rectangular area in the output grid
    # Ensure indices are within grid bounds (although numpy slicing handles this somewhat)
    draw_start_row = max(0, out_min_row)
    draw_end_row = min(rows, out_max_row + 1)
    draw_start_col = max(0, out_min_col)
    draw_end_col = min(cols, out_max_col + 1)
    
    if draw_start_row < draw_end_row and draw_start_col < draw_end_col:
        output_grid[draw_start_row:draw_end_row, draw_start_col:draw_end_col] = color

    # Return as list of lists
    return output_grid.tolist()
```