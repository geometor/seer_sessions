```python
import numpy as np
from typing import Tuple, List, Optional

"""
Identifies the single horizontal and single vertical line spanning the input grid.
Determines the color of these lines ('line_color') and their indices (row 'hr', column 'vc').
Identifies all pixels ('shape_pixels') that are not the background color (white, 0) and not the 'line_color'.
Creates a new output grid reduced in size by 1x1 compared to the input grid, initially filled with the background color.
For each 'shape_pixel' at (r, c) in the input:
  Calculates its relative position (dr, dc) to the intersection of the lines (hr, vc).
  Determines the four symmetric positions in the input grid relative to the intersection point:
    1. (hr + dr, vc + dc) - original position
    2. (hr + dr, vc - dc) - reflection across vertical line
    3. (hr - dr, vc + dc) - reflection across horizontal line
    4. (hr - dr, vc - dc) - reflection across both lines
  For each of these four input grid positions, calculates the corresponding position in the smaller output grid by adjusting for the removal of the row 'hr' and column 'vc'.
  Sets the color of these four calculated positions in the output grid to 'line_color'.
Returns the final output grid.
"""

def find_lines(grid: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the single horizontal and vertical lines.

    Args:
        grid: The input numpy array.

    Returns:
        A tuple (hr, vc, line_color) if found, else None.
        hr: row index of the horizontal line.
        vc: column index of the vertical line.
        line_color: the color of the lines.
    """
    height, width = grid.shape
    hr, vc, line_color = -1, -1, -1

    # Find horizontal line
    for r in range(height):
        first_color = grid[r, 0]
        if first_color != 0 and np.all(grid[r, :] == first_color):
            hr = r
            line_color = first_color
            break

    # Find vertical line
    for c in range(width):
        # Check if line_color has been set by horizontal search first
        if line_color != -1: 
             if grid[0, c] == line_color and np.all(grid[:, c] == line_color):
                 vc = c
                 break
        # If no horizontal line found yet, check for any non-background vertical line
        elif grid[0, c] != 0 and np.all(grid[:, c] == grid[0,c]):
             vc = c
             potential_line_color = grid[0,c]
             # Verify if horizontal line also exists with this color
             found_hr_match = False
             for r in range(height):
                 if grid[r,0] == potential_line_color and np.all(grid[r,:] == potential_line_color):
                     hr = r
                     line_color = potential_line_color
                     found_hr_match = True
                     break
             if found_hr_match:
                 break # Found both lines

    if hr != -1 and vc != -1 and line_color != -1:
         # Final check: ensure the identified vertical line color matches the horizontal one if both found separately initially
         if grid[hr, vc] == line_color and np.all(grid[hr, :] == line_color) and np.all(grid[:, vc] == line_color):
            return hr, vc, line_color
         else:
             # This case might indicate inconsistent lines, handle as error/not found
              return None
    else:
        return None # Lines not found

def find_shape_pixels(grid: np.ndarray, line_color: int) -> List[Tuple[int, int]]:
    """
    Finds pixels that are not background (0) and not the line color.

    Args:
        grid: The input numpy array.
        line_color: The color of the identified lines.

    Returns:
        A list of (row, col) tuples for shape pixels.
    """
    shape_pixels = []
    height, width = grid.shape
    background_color = 0
    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and grid[r, c] != line_color:
                shape_pixels.append((r, c))
    return shape_pixels

def map_to_output_coords(r: int, c: int, hr: int, vc: int) -> Optional[Tuple[int, int]]:
    """
    Maps input grid coordinates to output grid coordinates, adjusting for removed lines.

    Args:
        r: Input row index.
        c: Input column index.
        hr: Row index of the removed horizontal line.
        vc: Column index of the removed vertical line.

    Returns:
        Tuple (out_r, out_c) of output coordinates, or None if the input coords are on the removed lines.
    """
    if r == hr or c == vc:
        return None # Points on the line are removed

    out_r = r if r < hr else r - 1
    out_c = c if c < vc else c - 1
    return out_r, out_c

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the described transformation: identifies lines, finds a shape,
    mirrors the shape across the lines into four quadrants in a smaller grid,
    and colors the mirrored shapes with the line color.
    """
    input_h, input_w = input_grid.shape
    
    # 1. Identify the lines and their properties
    line_info = find_lines(input_grid)
    if line_info is None:
        # Handle error: lines not found as expected
        # Depending on strictness, could return input, empty grid, or raise error
        print("Error: Could not find expected horizontal and vertical lines.")
        # Return empty grid of expected size as a guess
        return np.zeros((input_h - 1, input_w - 1), dtype=int) 
        
    hr, vc, line_color = line_info

    # 2. Identify shape pixels
    shape_pixels = find_shape_pixels(input_grid, line_color)

    # 3. Create the output grid
    output_h = input_h - 1
    output_w = input_w - 1
    output_grid = np.zeros((output_h, output_w), dtype=int) # Background color is 0

    # 4. Process each shape pixel
    for r, c in shape_pixels:
        # a. Calculate relative position to intersection
        dr = r - hr
        dc = c - vc

        # b/c. Determine the four symmetric positions in the input grid coordinates
        mirrored_input_coords = [
            (hr + dr, vc + dc), # Original quadrant relative position
            (hr + dr, vc - dc), # Mirror across V-line
            (hr - dr, vc + dc), # Mirror across H-line
            (hr - dr, vc - dc)  # Mirror across both (center)
        ]

        # d/e. Map to output grid and color
        for mir_r, mir_c in mirrored_input_coords:
             # Ensure the mirrored coordinates are within the bounds of the input grid technically,
             # although points derived from valid shape pixels should be. Redundant check for safety.
             if 0 <= mir_r < input_h and 0 <= mir_c < input_w:
                 output_coords = map_to_output_coords(mir_r, mir_c, hr, vc)
                 if output_coords is not None:
                     out_r, out_c = output_coords
                     # Final boundary check for output grid
                     if 0 <= out_r < output_h and 0 <= out_c < output_w:
                         output_grid[out_r, out_c] = line_color
                     # else: # This shouldn't happen if logic is correct
                     #     print(f"Warning: Calculated output coord ({out_r}, {out_c}) out of bounds.")

    # 5. Return the completed output grid
    return output_grid
```