import numpy as np
from typing import List, Tuple, Dict, Optional

"""
Identify all maximal horizontal contiguous segments (lines) of non-white (0) pixels in the input grid. 
Find the pair of lines that meet the following criteria: 
1. They have the same color.
2. They have the same start and end column indices.
3. They are in different rows.
4. They have the maximum width among all pairs satisfying the above conditions.
Extract the subgrid located vertically between the two lines (exclusive) and horizontally between the start and end columns of the lines (exclusive). The top row of the output is the row immediately below the top line of the pair, the bottom row is the row immediately above the bottom line of the pair. The left column is the column immediately to the right of the start column of the lines, and the right column is the column immediately to the left of the end column of the lines.
"""

Grid = List[List[int]]
Line = Tuple[int, int, int, int, int] # color, row, start_col, end_col, width

def find_horizontal_lines(grid: np.ndarray) -> List[Line]:
    """
    Finds all maximal horizontal lines of non-white pixels in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of tuples, where each tuple represents a line:
        (color, row_index, start_column, end_column, width).
    """
    lines = []
    rows, cols = grid.shape
    for r in range(rows):
        c = 0
        while c < cols:
            color = grid[r, c]
            if color != 0:
                start_c = c
                while c + 1 < cols and grid[r, c + 1] == color:
                    c += 1
                end_c = c
                width = end_c - start_c + 1
                lines.append((color, r, start_c, end_c, width))
            c += 1
    return lines

def transform(input_grid: Grid) -> Grid:
    """
    Transforms the input grid by finding the widest pair of identical, 
    vertically aligned horizontal lines and extracting the subgrid between them.

    Args:
        input_grid: The input grid as a list of lists.

    Returns:
        The transformed grid as a list of lists.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    
    if rows == 0 or cols == 0:
        return [] # Handle empty input

    # 1. Find all horizontal lines
    lines = find_horizontal_lines(grid_np)

    # 2. Find the widest pair of aligned lines
    max_width = -1
    best_pair: Optional[Tuple[Line, Line]] = None

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            line1 = lines[i]
            line2 = lines[j]

            color1, r1, sc1, ec1, w1 = line1
            color2, r2, sc2, ec2, w2 = line2

            # Check conditions: same color, same start/end columns, different rows
            if color1 == color2 and sc1 == sc2 and ec1 == ec2 and r1 != r2:
                # Check if this pair is wider than the current best
                if w1 > max_width:
                    max_width = w1
                    # Ensure order: top line first, bottom line second
                    if r1 < r2:
                        best_pair = (line1, line2)
                    else:
                        best_pair = (line2, line1)
                # If widths are equal, the problem description doesn't specify tie-breaking.
                # The current logic implicitly favors the pair encountered first, 
                # which aligns with the examples provided.

    # 3. If no such pair found, return empty grid (or handle as appropriate)
    if best_pair is None:
        # This case didn't occur in the examples, but it's good practice to handle.
        # Returning an empty grid might be one interpretation.
        return [[]] 

    # 4. Extract coordinates from the best pair
    top_line, bottom_line = best_pair
    _, r_top, c_start, c_end, _ = top_line
    _, r_bottom, _, _, _ = bottom_line # Use coordinates from top_line as they are identical

    # 5. Calculate subgrid boundaries
    output_r_start = r_top + 1
    output_r_end = r_bottom - 1 # Inclusive index for slicing is r_bottom
    output_c_start = c_start + 1
    output_c_end = c_end - 1   # Inclusive index for slicing is c_end

    # 6. Check for invalid dimensions (lines too close or too narrow)
    if output_r_start > output_r_end or output_c_start > output_c_end:
         # This case also didn't occur in examples but indicates no space between lines/columns.
         # Return an empty grid. The slicing below handles this naturally if end < start.
         return [[]]

    # 7. Extract the subgrid
    # Numpy slicing is [start_row:end_row_exclusive, start_col:end_col_exclusive]
    output_grid_np = grid_np[output_r_start : output_r_end + 1, output_c_start : output_c_end + 1]

    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid