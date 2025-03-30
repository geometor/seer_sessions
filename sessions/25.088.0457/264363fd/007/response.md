```python
import numpy as np

"""
Transformation Rule:
1.  Identify the frame color (gray, 5) and the inner color (blue, 1).
2.  Find the lowest row index (`max_r_inner`) containing the inner color (blue, 1).
3.  Find the highest row index (`min_r_frame`) containing the frame color (gray, 5).
4.  Copy the input grid to create the output grid.
5.  Duplicate the row `max_r_inner` from the input grid to row `max_r_inner + 1` in the output grid.
6.  Duplicate the row `min_r_frame` from the input grid to row `min_r_frame - 1` in the output grid.
"""

def find_first_row_with_color(grid, color, search_from_top=True):
    """
    Finds the index of the first row containing the specified color.
    Searches from top to bottom if search_from_top is True, otherwise bottom to top.
    Returns -1 if the color is not found.
    """
    rows, _ = grid.shape
    if search_from_top:
        for r in range(rows):
            if color in grid[r, :]:
                return r
    else:
        for r in range(rows - 1, -1, -1):
            if color in grid[r, :]:
                return r
    return -1 # Color not found in any row

def transform(input_grid_list):
    """
    Applies the transformation: duplicates the lowest row containing the inner
    color (1) downwards by one, and duplicates the topmost row containing the
    frame color (5) upwards by one.
    """
    input_grid = np.array(input_grid_list)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Define the colors of interest
    frame_color = 5 # gray
    inner_color = 1 # blue

    # Find the lowest row index containing the inner color (search from bottom)
    max_r_inner = find_first_row_with_color(input_grid, inner_color, search_from_top=False)

    # Find the highest row index containing the frame color (search from top)
    min_r_frame = find_first_row_with_color(input_grid, frame_color, search_from_top=True)

    # Apply the duplication if the rows are found and within bounds
    # Check if the target rows for duplication are valid indices
    if max_r_inner != -1 and (max_r_inner + 1) < rows:
        # Copy the lowest inner row downwards
        output_grid[max_r_inner + 1, :] = input_grid[max_r_inner, :]

    if min_r_frame != -1 and (min_r_frame - 1) >= 0:
        # Copy the topmost frame row upwards
        # Important: Use the original input_grid for the source row,
        # in case the downwards copy overwrote part of the original frame row
        # if max_r_inner == min_r_frame - 1.
        output_grid[min_r_frame - 1, :] = input_grid[min_r_frame, :]

    return output_grid.tolist()
```