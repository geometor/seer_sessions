"""
Transforms input grids to output grids based on the position of gray (5) pixels and row sections.
The transformation identifies contiguous groups of black pixels in reference rows and applies color changes
to the corresponding columns within each section, only if there are black pixels in those columns within the reference rows.

1.  **Find Separator Rows:** Identify all rows that are completely gray (5).
2.  **Define Sections:** Divide into sections (top, middle, bottom) based on gray rows.
3.  **Identify Reference Rows and Contiguous Black Pixels:**
    *   Top: First row.
    *   Middle: Row after the first gray row.
    *   Bottom: Row after the second gray row.
    Identify contiguous black pixel columns in each reference row.
4.  **Transform Sections:** Change black pixels in the specified columns *only if* they are in the same column as a black pixel in the reference row:
    *   Top: Change to blue (1).
    *   Middle: Change to red (2).
    *   Bottom: Change to green (3).
5.  **Preserve Other Pixels:** All other pixels remain unchanged.
"""

import numpy as np

def find_all_gray_rows(grid):
    """Finds rows that are entirely filled with gray (5) pixels."""
    gray_rows = []
    for i, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            gray_rows.append(i)
    return gray_rows

def find_contiguous_black_columns(row):
    """Finds the starting and ending columns where contiguous black (0) pixels exist in a given row."""
    cols = []
    i = 0
    while i < len(row):
        if row[i] == 0:
            j = i
            while j < len(row) and row[j] == 0:
                j += 1
            cols.append((i, j -1)) # Store start and end indices
            i = j
        else:
            i += 1
    return cols

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find gray separator rows
    all_gray_rows = find_all_gray_rows(input_grid)

    # Top section transformation
    if len(all_gray_rows) >= 1:
        top_ref_row = input_grid[0]
        top_cols_ranges = find_contiguous_black_columns(top_ref_row)
        for r in range(0, all_gray_rows[0]):
            for start, end in top_cols_ranges:
                for c in range(start, end + 1):
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = 1

    # Middle section transformation
    if len(all_gray_rows) >= 1:
        if len(all_gray_rows) > 1:
            middle_ref_row = input_grid[all_gray_rows[0] + 1]
            start_row = all_gray_rows[0] + 1
            end_row = all_gray_rows[1]
        else:
            middle_ref_row = input_grid[all_gray_rows[0] + 1]
            start_row = all_gray_rows[0] + 1
            end_row = rows
        middle_cols_ranges = find_contiguous_black_columns(middle_ref_row)

        for r in range(start_row, end_row):
            for start, end in middle_cols_ranges:
                for c in range(start, end + 1):
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = 2

    # Bottom section transformation
    if len(all_gray_rows) >= 2:
        bottom_ref_row = input_grid[all_gray_rows[1] + 1]
        bottom_cols_ranges = find_contiguous_black_columns(bottom_ref_row)
        for r in range(all_gray_rows[1] + 1, rows):
            for start, end in bottom_cols_ranges:
                for c in range(start, end + 1):
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = 3

    return output_grid.tolist()