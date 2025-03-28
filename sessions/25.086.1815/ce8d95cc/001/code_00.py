import numpy as np
from typing import List, Tuple

"""
Extract structural information by identifying vertical and horizontal lines and their intersections, 
condensing the grid based on these features.

1.  Identify Horizontal Lines: Scan the input grid row by row. Identify rows where all non-white (0) pixels share the same color, and there is at least one non-white pixel. Record the row index and the color for each horizontal line found.
2.  Identify Vertical Lines: Scan the input grid column by column. For each column, examine the pixels in rows that are *not* identified as horizontal lines. If all non-white pixels in these examined rows share the same color, and there is at least one such non-white pixel, identify this column as a vertical line column. Record the column index and the color for each vertical line found. Keep track of the order of vertical lines from left to right.
3.  Determine Output Dimensions: Calculate the output grid height as `2 * (number of horizontal lines) + 1` and the width as `2 * (number of vertical lines) + 1`.
4.  Initialize Output Grid: Create an output grid of the calculated dimensions, initialized with white (0).
5.  Populate Output Grid: Iterate through the rows (`r_out`) and columns (`c_out`) of the output grid.
    *   If `r_out` is even (Segment Row): 
        *   Set even columns (`c_out % 2 == 0`) to white (0).
        *   Set odd columns (`c_out % 2 != 0`) to the color of the corresponding vertical line (`v_lines[c_out // 2][1]`).
    *   If `r_out` is odd (Horizontal Line Row):
        *   Let this correspond to the `k`-th horizontal line (`k = r_out // 2`) with input row index `r_in` and color `H`.
        *   Set even columns (`c_out % 2 == 0`) to the horizontal line color `H`.
        *   Set odd columns (`c_out % 2 != 0`) to the color found at the intersection in the input grid: `input_grid[r_in][c_in]`, where `c_in` is the column index of the corresponding vertical line (`v_lines[c_out // 2][0]`).
6.  Return Output Grid.
"""


def find_horizontal_lines(grid: np.ndarray) -> List[Tuple[int, int]]:
    """
    Identifies rows that represent horizontal lines.
    A row is a horizontal line if it contains at least one non-white pixel, 
    and all non-white pixels in that row share the same color.
    Returns a list of tuples (row_index, color).
    """
    h_lines = []
    height, _ = grid.shape
    for r in range(height):
        row = grid[r, :]
        non_white_pixels = row[row != 0]
        if len(non_white_pixels) > 0:
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

    # If there are no segment rows (e.g., grid is all horizontal lines?), we can't find vertical lines this way.
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
    Transforms the input grid by extracting horizontal and vertical line structures.
    """
    grid = np.array(input_grid, dtype=int)
    
    # 1. Find Horizontal Lines
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
        is_h_line_row = r_out % 2 != 0
        
        if is_h_line_row:
            # This row represents a horizontal line from the input
            h_line_index_in_list = r_out // 2
            if h_line_index_in_list < len(h_lines):
                r_in, h_color = h_lines[h_line_index_in_list]
                separator_color = h_color
            else:
                # Should not happen if dimensions are calculated correctly
                separator_color = 0 # Default or error color
        else:
            # This row represents a segment between horizontal lines (or above/below)
            separator_color = 0 # White background for segments

        for c_out in range(output_width):
            is_v_line_col = c_out % 2 != 0

            if is_v_line_col:
                 # This column represents a vertical line from the input
                v_line_index_in_list = c_out // 2
                if v_line_index_in_list < len(v_lines):
                    c_in, v_color = v_lines[v_line_index_in_list]
                    
                    if is_h_line_row:
                        # Intersection pixel
                        # Ensure r_in is valid (from the h_lines check above)
                        if h_line_index_in_list < len(h_lines):
                             output_grid[r_out, c_out] = grid[r_in, c_in]
                        else:
                             output_grid[r_out, c_out] = 0 # Error case? Default to background
                    else:
                        # Segment pixel - use the vertical line's color
                        output_grid[r_out, c_out] = v_color
                else:
                     # Should not happen
                     output_grid[r_out, c_out] = 0 

            else:
                # This column is a separator column
                output_grid[r_out, c_out] = separator_color

    # 6. Return Output Grid as list of lists
    return output_grid.tolist()