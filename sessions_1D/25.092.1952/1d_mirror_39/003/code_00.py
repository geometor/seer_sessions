"""
Transforms an input grid based on the following rules:
1. Create the output grid with the same dimensions as the input grid, initializing all pixels to white (0).
2. Find the coordinates (`maroon_row`, `maroon_col`) of the single maroon (9) pixel in the input grid.
3. Place a maroon (9) pixel at the same coordinates (`maroon_row`, `maroon_col`) in the output grid.
4. Identify the color (`shape_color`) of the contiguous shape that is not white (0) or maroon (9).
5. Collect the set of all coordinates `(r, c)` in the input grid that have the `shape_color`. These form the "movable shape".
6. If no movable shape is found, return the output grid containing only the maroon pixel.
7. Determine the minimum row index (`shape_top_row`) among all coordinates belonging to the movable shape.
8. For each coordinate `(r, c)` belonging to the movable shape in the input grid:
    a. Calculate the pixel's vertical offset from the top of its shape: `relative_r = r - shape_top_row`.
    b. Calculate the pixel's target row in the output grid: `new_r = (maroon_row + 1) + relative_r`.
    c. Set the pixel at coordinate (`new_r`, `c`) in the output grid to the `shape_color`.
9. Return the completed output grid.
"""

import numpy as np
from typing import List, Tuple, Optional, Set

def find_pixel(grid: np.ndarray, color: int) -> Optional[Tuple[int, int]]:
    """Finds the coordinates (row, col) of the first pixel with the specified color."""
    rows, cols = np.where(grid == color)
    if len(rows) > 0:
        # ARC guarantees only one maroon pixel per grid in this task's examples
        return int(rows[0]), int(cols[0])
    return None

def find_colored_shape(grid: np.ndarray) -> Optional[Tuple[Set[Tuple[int, int]], int]]:
    """
    Finds the set of coordinates and the color of the single 
    non-white (0), non-maroon (9) contiguous shape.
    Returns None if no such shape exists.
    """
    shape_pixels: Set[Tuple[int, int]] = set()
    shape_color = -1 
    height, width = grid.shape

    # First pass to find the color of the shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0 and color != 9:
                shape_color = color
                break # Found the color, stop searching
        if shape_color != -1:
            break
            
    if shape_color == -1:
        return None # No shape found

    # Second pass to collect all pixels of that color
    for r in range(height):
        for c in range(width):
            if grid[r, c] == shape_color:
                shape_pixels.add((r, c))

    if not shape_pixels:
         # This case should theoretically not happen if shape_color was found,
         # but added for robustness.
        return None

    return shape_pixels, shape_color


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Create the output grid with the same dimensions, filled with white (0).
    output_grid = np.zeros_like(input_np)

    # 2. Find the coordinates of the single maroon (9) pixel.
    maroon_pos = find_pixel(input_np, 9)
    if maroon_pos is None:
        # If no maroon pixel, the transformation is undefined by the examples.
        # Returning the empty grid is a possible handling.
        print("Warning: Maroon pixel (9) not found in input.")
        return output_grid.tolist() 
    maroon_row, maroon_col = maroon_pos

    # 3. Place the maroon pixel in the output grid.
    output_grid[maroon_row, maroon_col] = 9

    # 4. & 5. Identify the colored shape's pixels and color.
    shape_info = find_colored_shape(input_np)
    
    # 6. If no movable shape is found, return the grid with only the maroon pixel.
    if shape_info is None:
        return output_grid.tolist() 
        
    shape_pixels, shape_color = shape_info

    # 7. Determine the top-most row of the shape.
    # Check if shape_pixels is empty (should be handled by shape_info check, but safe)
    if not shape_pixels:
         return output_grid.tolist()
    shape_top_row = min(r for r, c in shape_pixels)

    # 8. Calculate new positions and place the shape in the output grid.
    for r, c in shape_pixels:
        # a. Calculate relative row within the shape.
        relative_r = r - shape_top_row
        # b. Calculate the new row in the output grid.
        new_r = (maroon_row + 1) + relative_r
        
        # c. Set the pixel in the output grid, checking bounds.
        if 0 <= new_r < height and 0 <= c < width:
            output_grid[new_r, c] = shape_color
        else:
            # Handle cases where the moved shape goes out of bounds.
            # Based on examples, this shouldn't happen, but log if it does.
            print(f"Warning: Pixel ({r},{c}) maps to out-of-bounds ({new_r},{c})")
            pass 

    # 9. Return the resulting grid as a list of lists.
    return output_grid.tolist()