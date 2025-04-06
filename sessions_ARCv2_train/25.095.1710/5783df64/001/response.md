```python
import math # Although not strictly needed for this logic, good practice if math ops were complex

"""
Takes a 2D input grid (H x W) containing exactly nine non-zero digits (1-9) scattered among zeros.
Divides the input grid into 9 equal sub-regions arranged in a 3x3 structure.
Finds the single non-zero digit within each sub-region.
Constructs a 3x3 output grid where each cell (i, j) contains the non-zero digit found in the corresponding (i, j) sub-region of the input grid.
"""

def find_non_zero_in_region(grid: list[list[int]], start_row: int, end_row: int, start_col: int, end_col: int) -> int:
    """
    Searches a specified rectangular region within the grid for the single non-zero value.
    """
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r][c] != 0:
                return grid[r][c]
    # Should not happen based on problem description, but return 0 as a fallback
    return 0 

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by partitioning it into 3x3 regions and extracting the non-zero number from each.
    """
    # Get input grid dimensions
    H = len(input_grid)
    W = len(input_grid[0]) if H > 0 else 0

    # Calculate region dimensions
    # Assuming H and W are always multiples of 3 based on examples
    region_height = H // 3
    region_width = W // 3

    # Initialize output_grid (3x3)
    output_grid = [[0 for _ in range(3)] for _ in range(3)]

    # Iterate through the 3x3 grid of regions
    for i in range(3):  # Region row index
        for j in range(3):  # Region column index
            # Define the boundaries for the current region (i, j)
            start_row = i * region_height
            end_row = (i + 1) * region_height
            start_col = j * region_width
            end_col = (j + 1) * region_width

            # Find the non-zero number within this region
            non_zero_value = find_non_zero_in_region(input_grid, start_row, end_row, start_col, end_col)

            # Place the found number into the output grid at position (i, j)
            output_grid[i][j] = non_zero_value

    return output_grid
```