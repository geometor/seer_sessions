```python
import copy

"""
Transforms a 4x4 input grid by locating a central 2x2 block of non-zero digits 
and moving these digits to the four corners of an otherwise zero-filled 4x4 output grid.

The mapping is as follows:
- The top-left digit of the 2x2 block moves to the top-left corner (0,0) of the output.
- The top-right digit of the 2x2 block moves to the top-right corner (0,3) of the output.
- The bottom-left digit of the 2x2 block moves to the bottom-left corner (3,0) of the output.
- The bottom-right digit of the 2x2 block moves to the bottom-right corner (3,3) of the output.
"""

def _find_nonzero_block_top_left(grid: list[list[int]]) -> tuple[int, int]:
    """
    Finds the top-left corner coordinates (row, col) of the 2x2 non-zero block
    within the input grid. Assumes the block is centrally located and not touching
    the outer border.
    """
    rows = len(grid)
    cols = len(grid[0])
    # Search the inner 2x2 area for the start of the block
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] != 0:
                # Assuming the first non-zero element found in the central region
                # is the top-left corner of the 2x2 block.
                return r, c
    # Return an indicator if the block wasn't found (based on assumptions)
    # This case should ideally not occur given the problem description.
    return -1, -1 

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Initialize a new 4x4 grid with all cells set to 0.
    output_grid = [[0 for _ in range(4)] for _ in range(4)]

    # 2. Locate the 2x2 subgrid within the input grid that contains non-zero numbers.
    #    Find the coordinates of its top-left cell.
    start_row, start_col = _find_nonzero_block_top_left(input_grid)

    # Check if the block was found
    if start_row == -1:
        # Handle error or return default if block structure isn't met
        # For this task, we assume the block always exists as described.
        print("Warning: Non-zero block not found as expected.")
        return output_grid # Return the empty grid or raise an error

    # 3. Identify the four numbers within this 2x2 subgrid.
    top_left_val = input_grid[start_row][start_col]
    top_right_val = input_grid[start_row][start_col + 1]
    bottom_left_val = input_grid[start_row + 1][start_col]
    bottom_right_val = input_grid[start_row + 1][start_col + 1]

    # 4. Place the top-left value into the output grid's top-left corner.
    output_grid[0][0] = top_left_val

    # 5. Place the top-right value into the output grid's top-right corner.
    output_grid[0][3] = top_right_val

    # 6. Place the bottom-left value into the output grid's bottom-left corner.
    output_grid[3][0] = bottom_left_val

    # 7. Place the bottom-right value into the output grid's bottom-right corner.
    output_grid[3][3] = bottom_right_val

    # 8. Return the modified output grid.
    return output_grid

```