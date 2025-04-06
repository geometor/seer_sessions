```python
import numpy as np

"""
Identify the 2x2 subgrid within the 5x5 input grid that is composed entirely of the value '2'. Record the row and column index of its top-left cell (marker_row, marker_col).
Calculate the coordinates for a "source" 2x2 subgrid: the row index is marker_row, and the column index is marker_col - 3.
Extract the 2x2 subgrid from the input grid starting at these calculated source coordinates.
Rotate the extracted 2x2 source subgrid 90 degrees clockwise.
The resulting rotated 2x2 grid is the final output.
"""

def find_marker_block(grid: list[list[int]]) -> tuple[int, int]:
    """Finds the top-left coordinates of the 2x2 block of '2's."""
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r][c] == 2 and
                grid[r+1][c] == 2 and
                grid[r][c+1] == 2 and
                grid[r+1][c+1] == 2):
                return r, c
    raise ValueError("Marker block (2x2 of '2's) not found in the input grid.")

def extract_subgrid(grid: list[list[int]], row: int, col: int, height: int, width: int) -> list[list[int]]:
    """Extracts a subgrid of specified dimensions."""
    subgrid = []
    for r in range(row, row + height):
        if r < 0 or r >= len(grid):
             raise IndexError(f"Row index {r} out of bounds for grid height {len(grid)}")
        new_row = []
        for c in range(col, col + width):
            if c < 0 or c >= len(grid[0]):
                 raise IndexError(f"Column index {c} out of bounds for grid width {len(grid[0])}")
            new_row.append(grid[r][c])
        subgrid.append(new_row)
    return subgrid

def rotate_90_clockwise(grid: list[list[int]]) -> list[list[int]]:
    """Rotates a grid 90 degrees clockwise."""
    # Use numpy for efficient rotation
    np_grid = np.array(grid)
    rotated_np_grid = np.rot90(np_grid, k=-1) # k=-1 for clockwise rotation
    # Convert back to list of lists
    return rotated_np_grid.tolist()


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input 5x5 grid to a 2x2 output grid based on marker and source blocks.
    """
    # 1. Find the 2x2 marker block of '2's
    marker_row, marker_col = find_marker_block(input_grid)

    # 2. Calculate the source block's top-left coordinates
    source_row = marker_row
    source_col = marker_col - 3

    # 3. Extract the 2x2 source block
    # Assuming the source block will always be 2x2
    source_block = extract_subgrid(input_grid, source_row, source_col, 2, 2)

    # 4. Rotate the source block 90 degrees clockwise
    output_grid = rotate_90_clockwise(source_block)

    # 5. Return the resulting grid
    return output_grid
```