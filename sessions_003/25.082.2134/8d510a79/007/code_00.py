"""
1.  **Grey Row:** Identify the row containing only grey (5) pixels. Copy this row to the output grid at the same row index.
2.  **Black Row:** A row with all black pixels acts as terminator.
3.  **Pattern Identification:** In each non-grey row, identify "pattern segments." A pattern segment starts when a pixel is horizontally adjacent (either before *or* after) to a blue (1) or red (2) pixel.
4.  **Horizontal Pattern Duplication:** Duplicate the pattern, overwriting zeros, until the end of the row or non-zero pixels.
5.  **Vertical Pattern Propagation:** If a non-grey row forms a pattern, copy the *entire* row's pattern to the next row in the output, *unless* the next input row is all zeros (black).
6. **Vertical Propagation Termination:** Continue vertical propagation until an all-black input row is encountered or the end of the grid is reached.
"""

import numpy as np

def find_grey_row(grid):
    """Finds the index of the row containing only grey pixels."""
    for i, row in enumerate(grid):
        if all(pixel == 5 for pixel in row):
            return i
    return -1

def find_black_row(grid):
    """finds indexes of any rows that are all black pixels"""
    black_rows = []
    for i, row in enumerate(grid):
        if all(pixel == 0 for pixel in row):
            black_rows.append(i)
    return black_rows

def has_adjacent_blue_or_red(grid, row_idx, col_idx):
    """Checks if a pixel has a blue (1) or red (2) neighbor horizontally."""
    if col_idx > 0 and (grid[row_idx][col_idx-1] in (1, 2)):
        return True
    if col_idx < len(grid[row_idx]) - 1 and (grid[row_idx][col_idx+1] in (1, 2)):
        return True
    return False

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Grey Row
    grey_row_index = find_grey_row(input_grid)
    if grey_row_index != -1:
        output_grid[grey_row_index] = input_grid[grey_row_index]

    # 2. & 6. Black Rows (for termination) and Vertical Propagation
    black_rows = find_black_row(input_grid)
    
    last_pattern_row = None

    for i in range(rows):
        if i == grey_row_index:
            continue

        # 3. Pattern Identification and 4. Horizontal Duplication
        new_row = np.copy(input_grid[i]) # Start with the original row
        
        if not all(pixel == 0 for pixel in new_row): # if not a black row

            for j in range(cols):
                if has_adjacent_blue_or_red(input_grid, i, j):
                    new_row[j] = input_grid[i,j]

            # expand the pattern to the left
            for j in range(cols):
                if new_row[j] in (1,2):
                    k=j-1
                    while k >= 0 and new_row[k] == 0:
                        new_row[k] = new_row[k+1]
                        k -= 1
            # expand to the right
            for j in range(cols-1, -1, -1):
                if new_row[j] in (1,2):
                    k=j+1
                    while k < cols and new_row[k] == 0:
                        new_row[k] = new_row[k-1]
                        k += 1
            last_pattern_row = new_row


        # 5. Vertical Propagation
        if last_pattern_row is not None:
            if i > 0 and not all(pixel == 0 for pixel in input_grid[i-1]) :
                output_grid[i] = last_pattern_row
                continue

        output_grid[i] = new_row

    return output_grid.tolist()