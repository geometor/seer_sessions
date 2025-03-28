import numpy as np

"""
Identifies two distinct full-height vertical lines and two distinct full-width horizontal lines of solid, non-white color within the input grid. 
The output grid is the rectangular subgrid defined by the intersection of these lines, inclusive of the lines themselves.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Extracts a subgrid bounded by specific vertical and horizontal lines.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the extracted subgrid.
    """
    input_grid = np.array(input_grid) # Ensure input is a numpy array
    height, width = input_grid.shape

    vertical_line_cols = []
    horizontal_line_rows = []

    # 1. Scan for vertical lines
    for col_idx in range(width):
        column = input_grid[:, col_idx]
        unique_vals = np.unique(column)
        # Check if the column consists of a single, non-white color
        if len(unique_vals) == 1 and unique_vals[0] != 0:
            vertical_line_cols.append(col_idx)

    # 2. Scan for horizontal lines
    for row_idx in range(height):
        row_data = input_grid[row_idx, :]
        unique_vals = np.unique(row_data)
        # Check if the row consists of a single, non-white color
        if len(unique_vals) == 1 and unique_vals[0] != 0:
            horizontal_line_rows.append(row_idx)

    # Basic validation based on task description (expect exactly two of each)
    if len(vertical_line_cols) != 2 or len(horizontal_line_rows) != 2:
        # This case shouldn't happen based on the training examples,
        # but adding a safeguard or error handling might be useful
        # for more robust application. For now, we assume valid input.
        print(f"Warning: Expected 2 vertical and 2 horizontal lines, found {len(vertical_line_cols)} and {len(horizontal_line_rows)}")
        # Depending on requirements, could raise an error or return input/empty grid
        # raise ValueError("Could not find exactly two vertical and two horizontal boundary lines.")


    # 3. Determine the minimum and maximum column indices
    left_col = min(vertical_line_cols)
    right_col = max(vertical_line_cols)

    # 4. Determine the minimum and maximum row indices
    top_row = min(horizontal_line_rows)
    bottom_row = max(horizontal_line_rows)

    # 5. Create the output grid by slicing the input grid
    # Note: Slicing in numpy is exclusive for the end index, so add 1
    output_grid = input_grid[top_row : bottom_row + 1, left_col : right_col + 1]

    return output_grid