import numpy as np
from typing import List, Tuple

"""
Condense a grid by representing it as an intersection of significant horizontal and vertical lines.

1.  Identify Horizontal Lines: Scan the input grid row by row. Identify rows that are completely filled with a single non-white color. Record the row index and the color for each such horizontal line found.
2.  Identify Vertical Lines: Scan the input grid column by column. For each column, consider only the rows that were *not* identified as horizontal lines in step 1. Examine the pixels in this column within these specific rows. If there is at least one non-white pixel among them, and *all* non-white pixels share the same color, then identify this column as a vertical line. Record the column index and the shared color for each vertical line found, maintaining their left-to-right order.
3.  Determine Output Dimensions: Calculate the output grid height as 2 * (number of horizontal lines) + 1 and the width as 2 * (number of vertical lines) + 1.
4.  Initialize Output Grid: Create an output grid of the calculated dimensions, filled with white (0).
5.  Populate Output Grid: Iterate through the output grid cells (r_out, c_out).
    *   If r_out is odd and c_out is odd (Intersection Point): Fill with the color from the input grid at the intersection of the corresponding original horizontal line row and vertical line column.
    *   If r_out is odd and c_out is even (Horizontal Line Segment): Fill with the color of the corresponding horizontal line.
    *   If r_out is even and c_out is odd (Vertical Line Segment): Fill with the color of the corresponding vertical line.
    *   If r_out is even and c_out is even (Background Corner): Leave as white (0).
6.  Return the populated output grid.
"""


def find_horizontal_lines(grid: np.ndarray) -> List[Tuple[int, int]]:
    """
    Identifies rows that are completely filled with a single non-white color.
    Returns a list of tuples (row_index, color).
    """
    h_lines = []
    height, width = grid.shape
    for r in range(height):
        row = grid[r, :]
        non_white_pixels = row[row != 0]
        # Check if the row contains any non-white pixels
        if len(non_white_pixels) > 0:
            # Check if all pixels in the row are non-white (i.e., length matches width)
            # and if all these non-white pixels are the same color
            if len(non_white_pixels) == width:
                 first_color = non_white_pixels[0]
                 if np.all(non_white_pixels == first_color):
                     h_lines.append((r, first_color))
    return h_lines

def find_vertical_lines(grid: np.ndarray, h_line_indices: List[int]) -> List[Tuple[int, int]]:
    """
    Identifies columns that represent vertical lines based on segments between horizontal lines.
    A column is a vertical line if, considering only rows *not* in h_line_indices,
    it contains at least one non-white pixel, and all such non-white pixels share the same color.
    Returns a list of tuples (column_index, color).
    """
    v_lines = []
    height, width = grid.shape
    h_line_set = set(h_line_indices)
    # Rows that are NOT horizontal lines (these define the segments)
    segment_rows = [r for r in range(height) if r not in h_line_set]

    # If there are no segment rows, we can't find vertical lines this way.
    if not segment_rows:
        return []

    for c in range(width):
        # Extract the part of the column that falls within the segments
        column_segment = grid[segment_rows, c]
        non_white_pixels = column_segment[column_segment != 0]
        if len(non_white_pixels) > 0:
            first_color = non_white_pixels[0]
            if np.all(non_white_pixels == first_color):
                v_lines.append((c, first_color))
    return v_lines

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on horizontal and vertical line structures.
    """
    grid = np.array(input_grid, dtype=int)

    # 1. Find Horizontal Lines (rows completely filled with one non-white color)
    h_lines = find_horizontal_lines(grid)
    h_line_indices = [r for r, c in h_lines]

    # 2. Find Vertical Lines (based on segments between horizontal lines)
    v_lines = find_vertical_lines(grid, h_line_indices)

    # 3. Determine Output Dimensions
    output_height = 2 * len(h_lines) + 1
    output_width = 2 * len(v_lines) + 1

    # 4. Initialize Output Grid (default to white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 5. Populate Output Grid
    for r_out in range(output_height):
        is_intersection_row = r_out % 2 != 0 # Corresponds to an h_line

        for c_out in range(output_width):
            is_intersection_col = c_out % 2 != 0 # Corresponds to a v_line

            h_idx = r_out // 2
            v_idx = c_out // 2

            # Ensure indices are valid before accessing h_lines/v_lines
            valid_h_idx = 0 <= h_idx < len(h_lines)
            valid_v_idx = 0 <= v_idx < len(v_lines)

            if is_intersection_row and is_intersection_col:
                # Case 1: Intersection Point (r_out odd, c_out odd)
                if valid_h_idx and valid_v_idx:
                    r_in = h_lines[h_idx][0]
                    c_in = v_lines[v_idx][0]
                    # Check if input indices are within bounds (safety check)
                    if 0 <= r_in < grid.shape[0] and 0 <= c_in < grid.shape[1]:
                         output_grid[r_out, c_out] = grid[r_in, c_in]
                    # else: remains 0 (white) - should not happen with valid indices

            elif is_intersection_row and not is_intersection_col:
                # Case 2: Horizontal Line Segment (r_out odd, c_out even)
                 if valid_h_idx:
                     h_color = h_lines[h_idx][1]
                     output_grid[r_out, c_out] = h_color
                 # else: remains 0 (white)

            elif not is_intersection_row and is_intersection_col:
                # Case 3: Vertical Line Segment (r_out even, c_out odd)
                if valid_v_idx:
                    v_color = v_lines[v_idx][1]
                    output_grid[r_out, c_out] = v_color
                # else: remains 0 (white)

            else: # not is_intersection_row and not is_intersection_col
                # Case 4: Background Corner (r_out even, c_out even)
                # Already initialized to 0 (white), so no action needed.
                pass

    # 6. Return Output Grid as list of lists
    return output_grid.tolist()