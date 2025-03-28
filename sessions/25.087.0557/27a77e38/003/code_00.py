import numpy as np
import copy

"""
Identifies a horizontal gray line within the input grid.
Determines the column corresponding to the center of this gray line.
Finds the cell directly above the center of the gray line (the 'reference cell').
Examines the horizontal neighbors (left and right) of the reference cell.
Determines the 'source color' based on these neighbors:
 - If both neighbors exist and have the same color, use that color.
 - Otherwise, if the left neighbor exists, use its color.
 - Otherwise, if the right neighbor exists, use its color.
 - Otherwise (no neighbors), use the color of the reference cell itself.
Copies this source color to the cell in the last row of the grid, aligned vertically with the center of the gray line.
All other pixels remain unchanged.
"""

def find_gray_line_row_and_center(grid):
    """
    Finds the row index of the horizontal gray line and its center column index.
    A gray line row contains only gray (5) and possibly white (0) pixels,
    with at least one gray pixel forming a contiguous segment.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (row_index, center_column_index) or (-1, -1) if not found.
    """
    num_rows, num_cols = grid.shape
    for r in range(num_rows):
        gray_indices = [c for c in range(num_cols) if grid[r, c] == 5]
        
        # Skip if no gray pixels in this row
        if not gray_indices:
            continue
            
        # Check if the row contains only gray (5) and white (0)
        only_gray_and_white = True
        for c in range(num_cols):
            if grid[r, c] != 5 and grid[r, c] != 0:
                only_gray_and_white = False
                break
        
        if not only_gray_and_white:
            continue

        # Check if the gray pixels form a contiguous segment
        min_gray_col = min(gray_indices)
        max_gray_col = max(gray_indices)
        if max_gray_col - min_gray_col + 1 == len(gray_indices):
            # Found the gray line row
            center_col = (min_gray_col + max_gray_col) // 2
            return r, center_col
            
    # Gray line not found according to criteria
    return -1, -1

def determine_source_color(grid, gray_row, center_col):
    """
    Determines the source color based on the neighbors of the cell
    above the gray line's center.

    Args:
        grid (np.ndarray): The input grid.
        gray_row (int): The row index of the gray line.
        center_col (int): The center column index of the gray line.

    Returns:
        int: The determined source color, or -1 if calculation is not possible
             (e.g., gray line is in the first row).
    """
    num_rows, num_cols = grid.shape
    ref_row = gray_row - 1

    # Check if the reference row is valid
    if ref_row < 0:
        # Cannot determine color based on row above if gray line is in row 0
        # This case doesn't occur in the provided examples.
        # Returning an error indicator.
        return -1 

    left_col = center_col - 1
    right_col = center_col + 1

    # Check validity of neighbor columns
    left_valid = left_col >= 0
    right_valid = right_col < num_cols

    left_color = None
    if left_valid:
        left_color = grid[ref_row, left_col]

    right_color = None
    if right_valid:
        right_color = grid[ref_row, right_col]

    # Apply priority logic
    if left_valid and right_valid and left_color == right_color:
        # If both neighbors exist and have the same color, use that color.
        return left_color
    elif left_valid:
        # Else if the left neighbor exists, use its color.
        return left_color
    elif right_valid:
        # Else if the right neighbor exists, use its color.
        return right_color
    else:
        # Else (neither neighbor exists, e.g., 1-column wide grid affecting the reference row),
        # use the color of the reference cell itself.
        # Ensure center_col is valid (should be if gray line was found)
        if 0 <= center_col < num_cols:
             return grid[ref_row, center_col]
        else:
             # Should not happen if center_col was valid from find_gray_line...
             return -1 # Error indicator


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    num_rows, num_cols = output_grid.shape

    # 1. & 2. Identify the gray line row and its center column
    gray_row, center_col = find_gray_line_row_and_center(output_grid)

    # Handle error if gray line not found
    if gray_row == -1:
        print("Error: Gray line not found.")
        # Return the original grid if the prerequisite structure isn't met
        return input_grid 

    # 3. 4. & 5. Determine the source color based on neighbors above center
    source_color = determine_source_color(output_grid, gray_row, center_col)

    # Handle error if source color couldn't be determined
    if source_color == -1:
        print(f"Error: Could not determine source color (gray_row={gray_row}, center_col={center_col}).")
        # Return the original grid if logic fails
        return input_grid

    # 6. Identify the target cell coordinates
    target_row = num_rows - 1
    target_col = center_col

    # Ensure target coordinates are valid (redundant if center_col is valid)
    if 0 <= target_row < num_rows and 0 <= target_col < num_cols:
         # 7. Modify the output grid
         output_grid[target_row, target_col] = source_color
    else:
         # This case should ideally not be reached if previous steps succeeded
         print(f"Error: Invalid target coordinates ({target_row}, {target_col}).")
         return input_grid

    # Convert back to list of lists for the required output format
    return output_grid.tolist()