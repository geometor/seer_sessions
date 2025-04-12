import math
import json
import numpy as np

"""
Transforms a 3x3 input grid into a 9x9 output grid based on the relative positions of '3's to a central '2'.

1.  Initialize a 9x9 output grid with zeros.
2.  Locate the cell containing '2' in the input grid (marker cell).
3.  For each cell containing '3' in the input grid (context cell):
    a.  Calculate its position relative to the marker cell (dr, dc).
    b.  Map this relative position (dr, dc) to a specific top-left starting coordinate (start_row, start_col) for a 4x4 block in the output grid according to predefined rules.
    c.  Draw a 4x4 block filled with '3's at the determined starting coordinates in the output grid.
4.  Return the final 9x9 output grid.
"""

def find_value(grid: list[list[int]], value: int) -> tuple[int, int] | None:
    """Finds the row and column of the first occurrence of a value in the grid."""
    for r, row in enumerate(grid):
        for c, cell_value in enumerate(row):
            if cell_value == value:
                return r, c
    return None # Value not found

def draw_block(grid: list[list[int]], start_row: int, start_col: int, size: int, value: int) -> None:
    """Draws a square block of a given size and value onto the grid."""
    rows, cols = len(grid), len(grid[0])
    for r in range(start_row, min(start_row + size, rows)):
        for c in range(start_col, min(start_col + size, cols)):
            if 0 <= r < rows and 0 <= c < cols: # Check bounds just in case
                 grid[r][c] = value


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Generates a 9x9 output grid based on patterns indicated in a 3x3 input grid.
    The position of '2' acts as a center, and the relative positions of '3's
    determine where 4x4 blocks of '3's are placed in the output.
    """
    # Initialize a 9x9 output grid filled with 0s
    output_grid_size = 9
    output_grid = [[0 for _ in range(output_grid_size)] for _ in range(output_grid_size)]
    block_size = 4

    # Find the row and column coordinates (r2, c2) of the cell containing 2
    marker_pos = find_value(input_grid, 2)
    if marker_pos is None:
        # Handle cases where '2' might be missing, though not expected based on examples
        # For now, return the empty grid or raise an error. Let's return the empty grid.
        print("Warning: Marker value '2' not found in input grid.")
        return output_grid
    r2, c2 = marker_pos

    # Examine each cell (r, c) in the 3x3 input grid
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])
    for r in range(input_rows):
        for c in range(input_cols):
            # If the cell contains the value 3
            if input_grid[r][c] == 3:
                # Calculate the relative row difference dr = r - r2 and relative column difference dc = c - c2
                dr = r - r2
                dc = c - c2

                # Determine the top-left starting coordinates (start_row, start_col)
                # for placing a 4x4 block in the output grid based on (dr, dc)
                start_row, start_col = -1, -1 # Initialize with invalid values

                if (dr, dc) == (-1, -1) or (dr, dc) == (-1, 0):
                    start_row, start_col = 0, 0
                elif (dr, dc) == (0, 1) or (dr, dc) == (1, 0):
                     start_row, start_col = 1, 1
                #elif (dr, dc) == (-1, 0):  # Covered by first condition
                #    start_row, start_col = 0, 0
                elif (dr, dc) == (0, -1):
                    start_row, start_col = 4, 4
                #elif (dr, dc) == (1, 0): # Covered by second condition
                #    start_row, start_col = 1, 1
                elif (dr, dc) == (1, 1):
                    start_row, start_col = 5, 5
                # Add handling for other potential relative coordinates if needed,
                # though only these seem relevant from the examples.

                # Using the determined (start_row, start_col), fill a 4x4 area
                # in the target grid with the value 3.
                if start_row != -1 and start_col != -1: # Check if a valid mapping was found
                    draw_block(output_grid, start_row, start_col, block_size, 3)

    # Return the final 9x9 output grid
    return output_grid