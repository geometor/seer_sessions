import numpy as np
import copy

"""
Identifies horizontal and/or vertical separator lines composed entirely of the number 4.
The separator value is fixed at 4.
If a horizontal separator line is found at row index 'hr', the region of the grid above this line (rows 0 to hr-1) is considered the source pattern. This pattern is copied to the region below the separator line (rows hr+1 to end).
If a vertical separator line is found at column index 'vc', the region of the grid to the left of this line (columns 0 to vc-1) is considered the source pattern. This pattern is copied to the region to the right of the separator line (columns vc+1 to end).
If both a horizontal line (hr) and a vertical line (vc) are found, they divide the grid into four quadrants. The top-left quadrant (rows 0 to hr-1, columns 0 to vc-1) is the source pattern. This pattern is copied into the other three quadrants: top-right (rows 0 to hr-1, columns vc+1 to end), bottom-left (rows hr+1 to end, columns 0 to vc-1), and bottom-right (rows hr+1 to end, columns vc+1 to end).
The separator line(s) themselves remain unchanged in the output.
If no separator lines are found, the output grid is identical to the input grid.
When copying, if the source pattern is larger than the target region, the pattern is truncated to fit.
"""

def find_horizontal_separator(grid: np.ndarray, separator_value: int) -> int | None:
    """Finds the row index of the first horizontal separator line."""
    num_rows, _ = grid.shape
    for r in range(num_rows):
        if np.all(grid[r, :] == separator_value):
            return r
    return None

def find_vertical_separator(grid: np.ndarray, separator_value: int) -> int | None:
    """Finds the column index of the first vertical separator line."""
    _, num_cols = grid.shape
    for c in range(num_cols):
        if np.all(grid[:, c] == separator_value):
            return c
    return None

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on separator lines.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    grid = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy() 
    num_rows, num_cols = grid.shape
    separator_value = 4

    # Find separator lines
    hr = find_horizontal_separator(grid, separator_value)
    vc = find_vertical_separator(grid, separator_value)

    # Case 1: Both horizontal and vertical separators found
    if hr is not None and vc is not None:
        # Ensure the source pattern region actually exists (hr > 0 and vc > 0)
        if hr > 0 and vc > 0:
            # Extract source pattern (top-left quadrant)
            source_pattern = grid[0:hr, 0:vc]
            source_rows, source_cols = source_pattern.shape

            # --- Replicate pattern to other quadrants, carefully handling boundaries ---
            
            # Target: Top-right quadrant
            # Calculate target dimensions
            tr_rows = hr
            tr_cols = num_cols - (vc + 1)
            # Check if target quadrant exists and has positive dimensions
            if tr_rows > 0 and tr_cols > 0:
                # Determine the slice of the source pattern to copy (handle potential size mismatch)
                copy_rows = min(source_rows, tr_rows)
                copy_cols = min(source_cols, tr_cols)
                # Perform the copy
                output_grid[0:copy_rows, vc + 1 : vc + 1 + copy_cols] = source_pattern[0:copy_rows, 0:copy_cols]

            # Target: Bottom-left quadrant
            # Calculate target dimensions
            bl_rows = num_rows - (hr + 1)
            bl_cols = vc
            # Check if target quadrant exists and has positive dimensions
            if bl_rows > 0 and bl_cols > 0:
                # Determine the slice of the source pattern to copy
                copy_rows = min(source_rows, bl_rows)
                copy_cols = min(source_cols, bl_cols)
                # Perform the copy
                output_grid[hr + 1 : hr + 1 + copy_rows, 0:copy_cols] = source_pattern[0:copy_rows, 0:copy_cols]
                
            # Target: Bottom-right quadrant
             # Calculate target dimensions
            br_rows = num_rows - (hr + 1)
            br_cols = num_cols - (vc + 1)
            # Check if target quadrant exists and has positive dimensions
            if br_rows > 0 and br_cols > 0:
                # Determine the slice of the source pattern to copy
                copy_rows = min(source_rows, br_rows)
                copy_cols = min(source_cols, br_cols)
                # Perform the copy
                output_grid[hr + 1 : hr + 1 + copy_rows, vc + 1 : vc + 1 + copy_cols] = source_pattern[0:copy_rows, 0:copy_cols]

    # Case 2: Only horizontal separator found
    elif hr is not None:
        # Ensure the source pattern region exists (hr > 0)
        if hr > 0:
            # Extract source pattern (above the line)
            source_pattern = grid[0:hr, :]
            source_rows, source_cols = source_pattern.shape
            
            # Target: Region below the line
            # Calculate target dimensions
            target_rows = num_rows - (hr + 1)
            target_cols = num_cols
            # Check if target region exists and has positive dimensions
            if target_rows > 0 and target_cols > 0:
                # Determine the slice of the source pattern to copy
                copy_rows = min(source_rows, target_rows)
                # Perform the copy (all columns)
                output_grid[hr + 1 : hr + 1 + copy_rows, :] = source_pattern[0:copy_rows, :]

    # Case 3: Only vertical separator found
    elif vc is not None:
        # Ensure the source pattern region exists (vc > 0)
        if vc > 0:
            # Extract source pattern (left of the line)
            source_pattern = grid[:, 0:vc]
            source_rows, source_cols = source_pattern.shape

            # Target: Region right of the line
            # Calculate target dimensions
            target_rows = num_rows
            target_cols = num_cols - (vc + 1)
             # Check if target region exists and has positive dimensions
            if target_rows > 0 and target_cols > 0:
                 # Determine the slice of the source pattern to copy
                copy_cols = min(source_cols, target_cols)
                # Perform the copy (all rows)
                output_grid[:, vc + 1 : vc + 1 + copy_cols] = source_pattern[:, 0:copy_cols]


    # Case 4: No separators found - output_grid remains the initial copy of input_grid

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()