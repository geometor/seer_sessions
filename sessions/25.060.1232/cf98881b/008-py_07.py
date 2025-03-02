"""
1.  **Identify Target Colors:** The target colors are Maroon (9), Yellow (4), White (0), and Yellow (4), in that order.

2.  **Find Matching Columns:**
    *   Find a column in the input grid that contains the color Maroon (9).
    *   Find a column in the input grid that contains the color Yellow (4).
    *   Find a column in the input grid that contains the color White (0).
    *   Find another, distinct column that contains the color Yellow (4).

3.  **Determine Output Height:** The height of the output grid is determined by the shortest length of the *found* columns, where *found* means they contain the target color. If a color is not found the length of that column is not considered.

4. **Select Columns for Output:** Select subcolumns to build the output. If any target colors where not found in the input grid, then an empty column (all zeros) is used.

5.  **Construct Output Grid:** Combine the selected columns in the order Maroon, Yellow, White, Yellow, to form the output grid. The output grid will have 4 columns.
"""

import numpy as np

def find_column(grid, color):
    """Finds a column that contains the specified color."""
    grid = np.array(grid)
    num_cols = grid.shape[1]
    for j in range(num_cols):
        if color in grid[:, j]:
            return grid[:, j].tolist()
    return None  # Return None if color not found

def find_second_yellow_column(grid):
    """Finds the second column containing yellow (4)."""
    grid = np.array(grid)
    num_cols = grid.shape[1]
    yellow_count = 0
    for j in range(num_cols):
        if 4 in grid[:, j]:
            yellow_count += 1
            if yellow_count == 2:
                return grid[:, j].tolist()
    return None

def transform(input_grid):
    # 1. & 2. Find Matching Columns
    maroon_col = find_column(input_grid, 9)
    yellow_col_1 = find_column(input_grid, 4)
    white_col = find_column(input_grid, 0)
    yellow_col_2 = find_second_yellow_column(input_grid)

    # 3. Determine Output Height
    found_cols = []
    if maroon_col is not None:
        found_cols.append(maroon_col)
    if yellow_col_1 is not None:
        found_cols.append(yellow_col_1)
    if white_col is not None:
        found_cols.append(white_col)
    if yellow_col_2 is not None:
        found_cols.append(yellow_col_2)
    
    if not found_cols:
        output_height = 0
    else:
        output_height = min(len(col) for col in found_cols)

    # 4. Select Columns for Output (handle None and truncate)
    default_col = [0] * output_height
    maroon_col = (maroon_col if maroon_col is not None else default_col)[:output_height]
    yellow_col_1 = (yellow_col_1 if yellow_col_1 is not None else default_col)[:output_height]
    white_col = (white_col if white_col is not None else default_col)[:output_height]
    yellow_col_2 = (yellow_col_2 if yellow_col_2 is not None else default_col)[:output_height]
  
    # 5. Construct Output Grid
    if output_height > 0:
        output_grid = np.array([
            maroon_col,
            yellow_col_1,
            white_col,
            yellow_col_2,
        ]).T
    else:
        output_grid = np.array([])

    return output_grid.tolist()