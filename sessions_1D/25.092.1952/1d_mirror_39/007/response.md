```python
import numpy as np
from typing import List, Tuple, Optional, Set

"""
Transforms an input grid based on the following rules:
1. Initialize the output grid with the same dimensions as the input grid, filling it entirely with white pixels (0).
2. Find the coordinates (`marker_row`, `marker_col`) of the single maroon pixel (9) (the marker) in the input grid.
3. Place a maroon pixel (9) at the same coordinates (`marker_row`, `marker_col`) in the output grid.
4. Identify the unique color (`shape_color`) present in the input grid that is neither white (0) nor maroon (9).
5. Collect the set of all coordinates `(r, c)` in the input grid where the pixel value is equal to `shape_color`. These coordinates constitute the "movable shape".
6. If no movable shape pixels are found (i.e., the set of coordinates is empty), return the output grid containing only the white background and the single maroon pixel.
7. Determine the minimum row index (`shape_top_row`) among all coordinates collected in step 5.
8. For each coordinate `(r, c)` belonging to the movable shape (from the set collected in step 5):
    a. Calculate the pixel's vertical offset relative to the top of its shape: `relative_r = r - shape_top_row`.
    b. Calculate the pixel's target row in the output grid: `new_r = (marker_row + 1) + relative_r`.
    c. Check if the target coordinate (`new_r`, `c`) is within the output grid boundaries.
    d. If it is within bounds, set the pixel at (`new_r`, `c`) in the output grid to `shape_color`.
9. Return the completed output grid.
"""

def find_pixel(grid: np.ndarray, color: int) -> Optional[Tuple[int, int]]:
    """
    Finds the coordinates (row, col) of the first pixel matching the given color.
    Assumes at most one such pixel exists for the marker color (9).
    Returns None if the color is not found.
    """
    rows, cols = np.where(grid == color)
    if len(rows) > 0:
        return int(rows[0]), int(cols[0])
    return None

def find_movable_shape(grid: np.ndarray) -> Optional[Tuple[Set[Tuple[int, int]], int]]:
    """
    Identifies the color and collects the coordinates of the single movable shape.
    The movable shape's color is the unique color in the grid that is not 0 (white) or 9 (maroon).
    Returns a tuple (set_of_coordinates, shape_color), or None if no such shape exists.
    """
    # Find unique colors excluding background (0) and marker (9)
    possible_colors = set(np.unique(grid)) - {0, 9}

    if not possible_colors:
        return None # No shape color found

    # Assume only one shape color based on task examples
    if len(possible_colors) > 1:
        # Handle unexpected case: multiple potential shape colors.
        # Based on observation, this shouldn't happen. We might default to one,
        # but returning None or raising an error might be safer depending on requirements.
        # For now, let's assume the task guarantees only one shape color.
        # If we had to choose, maybe min(possible_colors) is a strategy.
         print(f"Warning: Found multiple non-background, non-marker colors: {possible_colors}. This case is ambiguous based on examples.")
         # Let's choose the numerically smallest color as the shape color
         shape_color = min(possible_colors)
    else:
        shape_color = possible_colors.pop()

    # Collect all pixels of that shape color
    shape_pixels: Set[Tuple[int, int]] = set()
    rows, cols = np.where(grid == shape_color)
    for r, c in zip(rows, cols):
         shape_pixels.add((int(r), int(c)))

    if not shape_pixels:
        # This shouldn't happen if shape_color was found, but included as a safeguard
        return None

    return shape_pixels, shape_color

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Initialize the output grid with the same dimensions, filled with white (0).
    output_grid = np.zeros_like(input_np)

    # 2. Find the coordinates of the single maroon (9) pixel (marker).
    marker_pos = find_pixel(input_np, 9)
    if marker_pos is None:
        # If no marker pixel, the transformation is undefined by the examples.
        # Return the empty grid as a fallback.
        print("Warning: Marker pixel (9) not found in input.")
        return output_grid.tolist()
    marker_row, marker_col = marker_pos

    # 3. Place the marker pixel in the output grid.
    output_grid[marker_row, marker_col] = 9

    # 4. & 5. Identify the movable shape's pixels and color.
    shape_info = find_movable_shape(input_np)

    # 6. If no movable shape is found, return the grid with only the marker pixel.
    if shape_info is None:
        return output_grid.tolist()

    shape_pixels, shape_color = shape_info

    # 7. Determine the top-most row of the shape in the input grid.
    # We need shape_pixels to be non-empty here, ensured by check in find_movable_shape
    # and the shape_info is None check above.
    shape_top_row = min(r for r, c in shape_pixels)

    # 8. Calculate new positions and place the shape in the output grid.
    for r, c in shape_pixels:
        # a. Calculate the pixel's vertical offset from the top of its shape.
        relative_r = r - shape_top_row
        # b. Calculate the pixel's target row in the output grid.
        # The shape starts at the row immediately below the marker row.
        new_r = (marker_row + 1) + relative_r

        # c. & d. Check bounds and set the pixel in the output grid.
        if 0 <= new_r < height and 0 <= c < width:
            output_grid[new_r, c] = shape_color
        else:
            # Log if a pixel would be placed out of bounds (optional)
            # print(f"Debug: Pixel ({r},{c}) maps to out-of-bounds ({new_r},{c})")
            pass # Ignore pixels that move out of the grid boundaries

    # 9. Return the completed output grid as a list of lists.
    return output_grid.tolist()
```