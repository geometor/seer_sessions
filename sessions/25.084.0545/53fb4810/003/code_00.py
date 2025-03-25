"""
1.  **Iterate** through each column of the input grid.
2.  **Identify** "target columns": For each column, check if *all* its pixels are either azure (8) or red (2). If they are, then check if there are at least two consecutive red (2) pixels within that column.
3. **Insert**: If a column meets both criteria (all azure/red AND at least two consecutive reds), insert a new column immediately to the *left* of it.
4.  **Populate New Column:** The inserted column should alternate between yellow (4) and red (2) pixels. The very first inserted column across all examples starts with yellow (4), the next inserted column starts with red (2) and so on. This pattern repeats to fill the entire height of the new column.
"""

import numpy as np

def _find_target_columns(grid):
    """Identifies columns that contain only azure (8) and red (2) pixels, and have at least two consecutive red pixels."""
    target_columns = []
    for j in range(grid.shape[1]):
        is_azure_red = True
        has_consecutive_reds = False
        for i in range(grid.shape[0]):
            if grid[i, j] != 8 and grid[i, j] != 2:
                is_azure_red = False
                break  # Exit inner loop if a non-azure/red pixel is found
        if is_azure_red:
            for i in range(grid.shape[0] - 1):
                if grid[i, j] == 2 and grid[i+1, j] == 2:
                    has_consecutive_reds = True
                    break # Exit this check once two consecutive reds found.
        if is_azure_red and has_consecutive_reds:
                target_columns.append(j)
    return target_columns

def _insert_new_column(grid, col_index, insert_count):
    """Inserts a new column to the left of col_index, alternating yellow (4) and red (2)."""
    height = grid.shape[0]
    new_column = np.zeros(height, dtype=int)
    # Start with yellow (4) for the first insertion, then alternate.
    start_color = 4 if (insert_count % 2 == 0) else 2
    for i in range(height):
        new_column[i] = start_color if (i % 2 == 0) else (6 - start_color)  # 6-start_color gives the alternating color.
    return np.insert(grid, col_index, new_column, axis=1)

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    grid = np.array(input_grid)
    output_grid = grid.copy()
    target_columns = _find_target_columns(grid)

    insert_count = 0
    # Iterate in reverse to avoid index shifting issues after insertion
    for col_index in reversed(target_columns):
        output_grid = _insert_new_column(output_grid, col_index, insert_count)
        insert_count += 1 # Increment count for each *insertion*, not each column

    return output_grid.tolist()