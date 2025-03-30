import numpy as np
from typing import List, Dict, Tuple, Optional

"""
Transformation Rule:

1.  Determine the dimensions (Height H, Width W) of the input grid.
2.  Identify the border color (B) from the input grid's frame (e.g., pixel at `[0, 0]`).
3.  Initialize a new output grid of dimensions HxW, filled entirely with the background color (0, white).
4.  Draw the border onto the output grid: Set row 0, row H-1, column 0, and column W-1 to the border color B. Handle edge cases for 1-pixel height/width grids.
5.  Iterate through the rows `r` from 1 to H-2 to find the anchor pixels:
    *   Check if the pixels at `(r, 1)` and `(r, 18)` exist and are identical.
    *   Check if this identical color is not the background color (0) and not the border color (B).
    *   If both conditions are met, record this color as the anchor color (C) and the row index as the anchor row (R). Stop searching once found.
6.  If no anchor pixels are found, return the output grid with only the border drawn.
7.  Draw a horizontal line onto the output grid using the anchor color (C). This line should be on the anchor row (R) and extend from column 1 to column 18 (inclusive).
8.  Select the specific H-like shape pattern, its center row offset (CRO), and its starting column (Col) based *only* on the anchor color (C) using the following mapping:
    *   If C is Orange (7): Pattern=[[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1]], CRO=2, Col=13.
    *   If C is Magenta (6): Pattern=[[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,1,1]], CRO=2, Col=2.
    *   If C is Red (2): Pattern=[[1,0,1],[0,1,0],[1,1,1],[0,1,0],[1,0,1]], CRO=2, Col=6.
    *   If C is Blue (1): Pattern=[[1,0,1],[1,1,1],[1,0,1]], CRO=1, Col=14.
9.  Calculate the starting row for placing the shape: `start_row = R - CRO`.
10. Draw the selected shape pattern onto the output grid. Place the top-left of the pattern at `(start_row, Col)`. Use the anchor color (C) for pixels corresponding to '1' in the pattern definition, leaving pixels corresponding to '0' as background. Ensure drawing stays within the grid boundaries.
11. Return the completed output grid.
"""


def _draw_border(grid: np.ndarray, border_color: int):
    """Draws a border onto the grid."""
    height, width = grid.shape
    if height > 0 and width > 0:
        grid[0, :] = border_color
        if height > 1:
            grid[-1, :] = border_color
        grid[:, 0] = border_color
        if width > 1:
            grid[:, -1] = border_color

def _find_anchor(input_np: np.ndarray, border_color: int) -> Optional[Tuple[int, int]]:
    """Finds the anchor color (C) and row (R)."""
    height, width = input_np.shape
    background_color = 0

    # Need at least 3 rows and 19 columns to have anchors at (r, 1) and (r, 18) with r > 0
    if height < 3 or width < 19:
        return None

    for r in range(1, height - 1):
        pixel1 = input_np[r, 1]
        pixel18 = input_np[r, 18]

        # Check if pixels match, are not background, and not border color
        if pixel1 == pixel18 and pixel1 != background_color and pixel1 != border_color:
            return pixel1, r  # Return anchor_color (C), anchor_row (R)

    return None # Anchors not found

def _draw_horizontal_line(grid: np.ndarray, row: int, start_col: int, end_col: int, color: int):
    """Draws a horizontal line on the grid."""
    height, width = grid.shape
    if 0 <= row < height:
        for c in range(start_col, end_col + 1):
            if 0 <= c < width:
                grid[row, c] = color

def _draw_shape(grid: np.ndarray, shape_pattern: np.ndarray, top_row: int, left_col: int, color: int):
    """Draws the shape pattern onto the grid."""
    height, width = grid.shape
    shape_height, shape_width = shape_pattern.shape

    for r_idx in range(shape_height):
        for c_idx in range(shape_width):
            # Check if the pixel in the shape pattern should be drawn (represented by 1)
            if shape_pattern[r_idx, c_idx] == 1:
                # Calculate the target coordinates in the output grid
                output_row = top_row + r_idx
                output_col = left_col + c_idx

                # Check bounds before drawing
                if 0 <= output_row < height and 0 <= output_col < width:
                    grid[output_row, output_col] = color


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule: identifies border and anchor pixels,
    then draws a border, a horizontal line, and a specific H-shape in the
    output grid based on the anchor pixel properties.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    background_color = 0

    # Handle empty input case
    if height == 0 or width == 0:
        return input_grid

    # 3. Initialize output_grid with background color
    output_np = np.full_like(input_np, background_color)

    # 2. Identify border color
    border_color = input_np[0, 0]

    # 4. Draw the border onto the output grid
    _draw_border(output_np, border_color)

    # 5. Find anchor pixels (color C, row R)
    anchor_info = _find_anchor(input_np, border_color)

    # 6. If no anchors found, return the grid with just the border
    if anchor_info is None:
        return output_np.tolist()

    anchor_color, anchor_row = anchor_info

    # 7. Draw the horizontal line
    _draw_horizontal_line(output_np, anchor_row, 1, 18, anchor_color)

    # 8. Define H-shapes, offsets, and start columns based on anchor color
    # Using 1 for shape pixels, 0 for background
    shape_definitions = {
        7: {'shape': np.array([[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1]]), 'offset': 2, 'col': 13}, # Orange
        6: {'shape': np.array([[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,1,1]]), 'offset': 2, 'col': 2}, # Magenta
        2: {'shape': np.array([[1,0,1],[0,1,0],[1,1,1],[0,1,0],[1,0,1]]), 'offset': 2, 'col': 6}, # Red
        1: {'shape': np.array([[1,0,1],[1,1,1],[1,0,1]]),             'offset': 1, 'col': 14}  # Blue
    }

    # Check if a shape is defined for the found anchor color
    if anchor_color not in shape_definitions:
        # Return grid with border and line if shape unknown (shouldn't happen based on examples)
        return output_np.tolist()

    # Get the definition for the specific anchor color
    selected_shape_info = shape_definitions[anchor_color]
    shape_pattern = selected_shape_info['shape']
    center_row_offset = selected_shape_info['offset']
    start_col = selected_shape_info['col']

    # 9. Calculate the starting row for the shape
    start_row = anchor_row - center_row_offset

    # 10. Draw the selected shape onto the output grid
    _draw_shape(output_np, shape_pattern, start_row, start_col, anchor_color)

    # 11. Convert back to list of lists for the required output format
    output_grid = output_np.tolist()
    return output_grid