"""
1.  **Identify Lines:** In the input grid, identify all horizontal and vertical lines that consist of pixels where *any* of the pixels are color 6 (magenta) or 8 (azure). A line is defined as all contiguous pixels in a row or column.
2.  **Handle Horizontal Lines:** If a horizontal line of color 6 or 8 is found, create a row in the output grid. The length of the row should be equal to the length of the original input row. The output row is a copy of the input row.
3.  **Handle Vertical Lines:** If a vertical line of color 6 or 8 is found, create a column in the output grid. The height of the column should equal to the height of the original input column. The output column is a copy of the input column.
4. **Handle no lines:** If no lines are identified, then the output grid is 0x0.
5. **Remove Duplicate Rows and Columns**: Eliminate any duplicate rows.
"""

import numpy as np

def find_lines(grid, colors):
    """Finds rows and columns containing specified colors."""
    rows = []
    cols = []
    grid_array = np.array(grid)
    height, width = grid_array.shape

    for r in range(height):
        if any(color in grid_array[r, :] for color in colors):
            rows.append(r)

    for c in range(width):
        if any(color in grid_array[:, c] for color in colors):
            cols.append(c)

    return rows, cols

def remove_duplicate_rows(grid_list):
    """Removes duplicate rows from a list of lists."""
    unique_rows = []
    for row in grid_list:
        if row not in unique_rows:
            unique_rows.append(row)
    return unique_rows


def transform(input_grid):
    """Transforms the input grid to the output grid based on line presence."""

    input_array = np.array(input_grid)
    target_colors = [6, 8]
    rows, cols = find_lines(input_grid, target_colors)

    # Handle no lines case.
    if not rows and not cols:
        return []

    output_rows = []
    # Handle horizontal lines.
    for row_index in rows:
        output_rows.append(input_array[row_index, :].tolist())
    
    # Handle vertical lines
    for col_index in cols:
        output_rows.append(input_array[:, col_index].reshape(1,-1).tolist()[0]) # reshape for consistent dimensions
    
    # remove duplicate rows
    output_rows = remove_duplicate_rows(output_rows)

    return output_rows