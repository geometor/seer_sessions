```python
import numpy as np
import copy

"""
Identifies a vertical line segment (value 8) and a horizontal line segment (value 2) in the input grid.
Determines the column of the vertical line and the row of the horizontal line.
Extends the vertical line to fill its column with 8s, except for the row occupied by the horizontal line.
Extends the horizontal line to fill its row with 2s, except for the column occupied by the vertical line.
Places the value 4 at the intersection of the extended row and column.
Original non-zero values are preserved unless overwritten by the intersection point (4).
"""

def find_line_coord(grid: np.ndarray, value: int) -> tuple[int | None, int | None]:
    """Finds the coordinates (row, col) of the first occurrence of a given value.
       Assumes value 2 defines the target row and value 8 defines the target column.
    """
    coords = np.where(grid == value)
    if len(coords[0]) > 0:
        if value == 2: # Horizontal line defines target row
            return coords[0][0], None # Return row index
        elif value == 8: # Vertical line defines target col
            return None, coords[1][0] # Return col index
    return None, None # Should not happen based on examples

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the line extension and intersection transformation to the input grid.
    """
    # Convert to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = copy.deepcopy(grid_np) # Initialize output grid as a copy
    height, width = grid_np.shape

    # --- Identification Step ---
    # Find the row index of the horizontal line (value 2)
    target_row, _ = find_line_coord(grid_np, 2)
    # Find the column index of the vertical line (value 8)
    _, target_col = find_line_coord(grid_np, 8)

    # Validate if lines were found (basic check)
    if target_row is None or target_col is None:
        # Handle cases where lines are missing if necessary,
        # but based on examples, they are always present.
        print("Warning: Could not find both lines (value 2 and 8).")
        return input_grid # Return original if structure is unexpected

    # --- Transformation Steps ---
    # 1. Extend Vertical Line (value 8)
    for r in range(height):
        # Fill with 8 if it's not the target row and the cell is currently background (0)
        if r != target_row and output_grid[r, target_col] == 0:
            output_grid[r, target_col] = 8

    # 2. Extend Horizontal Line (value 2)
    for c in range(width):
        # Fill with 2 if it's not the target column and the cell is currently background (0)
        if c != target_col and output_grid[target_row, c] == 0:
            output_grid[target_row, c] = 2

    # 3. Mark Intersection (value 4)
    # This overwrites any value currently at the intersection
    output_grid[target_row, target_col] = 4

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```