```python
import math

"""
Transforms an input grid based on Manhattan distance parity from a central '0'.

1. Identifies the background value (the non-zero integer) in the input grid.
2. Locates the position (row, column) of the '0' cell in the input grid.
3. Creates an output grid of the same dimensions as the input grid.
4. Iterates through each cell position (r, c) in the grid.
5. Calculates the Manhattan distance between the current cell (r, c) and the '0' cell's position.
6. If the Manhattan distance is even, the corresponding cell in the output grid is set to '0'.
7. If the Manhattan distance is odd, the corresponding cell in the output grid is set to the identified background value.
8. Returns the completed output grid.
"""

def find_zero_position(grid: list[list[int]]) -> tuple[int, int] | None:
    """Finds the row and column index of the first '0' found in the grid."""
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 0:
                return r, c
    return None # Should not happen based on problem description

def find_background_value(grid: list[list[int]], zero_pos: tuple[int, int]) -> int:
    """Finds the non-zero background value in the grid."""
    # Check a corner cell first, assuming it's not the zero cell
    if zero_pos != (0, 0) and grid[0][0] != 0:
        return grid[0][0]
    # If the top-left is zero, iterate to find the first non-zero
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value != 0:
                return value
    return -1 # Should not happen based on problem description

def calculate_manhattan_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    r1, c1 = pos1
    r2, c2 = pos2
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """Applies the Manhattan distance parity transformation to the input grid."""

    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Find the location of the '0'
    zero_pos = find_zero_position(input_grid)
    if zero_pos is None:
         # Handle cases where 0 might not be present, though constraints imply it is.
         # For now, maybe return a copy or raise error. Let's return a copy.
         print("Warning: No zero found in input grid.")
         return [row[:] for row in input_grid]
    zero_row, zero_col = zero_pos

    # Find the background value
    background_value = find_background_value(input_grid, zero_pos)

    # Initialize the output grid (can be done element by element)
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the Manhattan distance from the current cell to the '0' cell
            distance = calculate_manhattan_distance((r, c), (zero_row, zero_col))

            # Check if the distance is even or odd
            if distance % 2 == 0:
                # If even, set the output cell to 0
                output_grid[r][c] = 0
            else:
                # If odd, set the output cell to the background value
                output_grid[r][c] = background_value

    # Return the completed output grid
    return output_grid
```