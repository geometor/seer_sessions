```python
import copy

"""
Place specific values (3, 6, 7, 8) in an output grid based on the location of the value '2' in the input grid.
The output grid is initialized with zeros. The value '2' is located in the input grid.
Values are placed diagonally relative to the position of '2':
- 3 is placed top-left.
- 6 is placed top-right.
- 8 is placed bottom-left.
- 7 is placed bottom-right.
Placement only occurs if the target coordinates are within the grid boundaries.
"""

def find_value(grid: list[list[int]], value: int) -> tuple[int | None, int | None]:
    """Finds the row and column index of the first occurrence of a value in the grid."""
    rows = len(grid)
    if rows == 0:
        return None, None
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == value:
                return r, c
    return None, None # Value not found

def is_within_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    """Checks if coordinates (r, c) are within the grid dimensions."""
    return 0 <= r < rows and 0 <= c < cols

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by placing values 3, 6, 8, 7 diagonally
    relative to the position of the value 2, respecting grid boundaries.
    """
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Find the location of the value '2' in the input grid
    r_in, c_in = find_value(input_grid, 2)

    # If '2' is not found, return the empty grid (as per current examples)
    if r_in is None or c_in is None:
        return output_grid # Or handle as an error, depending on requirements

    # Define the relative offsets and their corresponding values
    # (dr, dc, value) -> (row_delta, col_delta, value_to_place)
    offsets = [
        (-1, -1, 3), # Top-Left
        (-1,  1, 6), # Top-Right
        ( 1, -1, 8), # Bottom-Left
        ( 1,  1, 7), # Bottom-Right
    ]

    # Iterate through each offset definition
    for dr, dc, value in offsets:
        # Calculate the target coordinates in the output grid
        r_out = r_in + dr
        c_out = c_in + dc

        # Check if the target coordinates are within the grid bounds
        if is_within_bounds(r_out, c_out, rows, cols):
            # Place the corresponding value at the target coordinates
            output_grid[r_out][c_out] = value

    return output_grid
```