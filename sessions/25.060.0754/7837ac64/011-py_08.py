"""
Transformation Rule:

1.  **Find First Occurrences:** Examine the input grid to find the row and column indices of the first occurrence of a blue (1) pixel and the first occurrence of a green (3) pixel.

2.  **Calculate Relative Position:**
    *   Calculate the difference in row indices (`row_diff` = green_row - blue_row).
    *   Calculate the difference in column indices (`col_diff` = green_col - blue_col).

3.  **Determine Output Grid Size:**
    *   Create a new output grid.
    * if `row_diff` is not zero: output grid is `abs(row_diff) + 1` rows
    * if `col_diff` is not zero: output grid is `abs(col_diff) + 1` columns
    * If any of `row_diff` or `col_diff` are zero, the size is determined by whichever is not zero.

4. **Populate Output Grid:**
   *    If the blue pixel was found, place a blue pixel (1) in the output grid at position (0, 0).
    *   If the green pixel was found:
        *  If the blue pixel was also found, place the green pixel (3) at the location in the output grid corresponding to the `row_diff` and `col_diff`:
           + if blue is before green: place at (row_diff, col_diff)
           + if green is before blue, iterate down the rows until green is placed.
        *   If only the green pixel was found, place green pixel (3) at (0,0).

5. Return the output grid.
"""

import numpy as np

def find_first_occurrence(grid, target_colors):
    """
    Finds the row and column indices of the first occurrence of target colors.

    Args:
        grid: input grid
        target_colors: list of colors we are searching for

    Returns:
        A tuple of tuples: ((row_1, col_1), (row_2, col_2)) for the first occurrence of each target color,
                           or (None, None) for a color if it's not found.
    """

    first_occurrences = {}
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value in target_colors and value not in first_occurrences:
                first_occurrences[value] = (row_index, col_index)

    for color in target_colors:
        if color not in first_occurrences:
            first_occurrences[color] = (None, None)  # Handle colors not found

    return (first_occurrences[target_colors[0]], first_occurrences[target_colors[1]])

def transform(input_grid):
    # Convert to numpy array
    input_array = np.array(input_grid)

    # Find first occurrences of blue (1) and green (3)
    blue_first, green_first = find_first_occurrence(input_array, [1, 3])

    # Calculate relative positions
    row_diff = green_first[0] - blue_first[0] if blue_first[0] is not None and green_first[0] is not None else None
    col_diff = green_first[1] - blue_first[1] if blue_first[1] is not None and green_first[1] is not None else None

    # Determine output grid size
    if row_diff is not None and col_diff is not None:
        rows = abs(row_diff) + 1 if row_diff!=0 else (input_array.shape[0] - blue_first[0] if blue_first[0] is not None else 0)
        cols = abs(col_diff) + 1 if col_diff!=0 else (input_array.shape[1] - blue_first[1] if blue_first[1] is not None else 0)

    elif blue_first[0] is not None:
        rows = input_array.shape[0] - blue_first[0]
        cols = input_array.shape[1] - blue_first[1]
    elif green_first[0] is not None:
        rows = input_array.shape[0] - green_first[0]
        cols = input_array.shape[1] - green_first[1]

    else:
        rows,cols = 0,0 # both not found
        return np.zeros((rows, cols), dtype=int).tolist()

    output_grid = np.zeros((rows, cols), dtype=int)

    # Populate output grid
    if blue_first[0] is not None:
        output_grid[0, 0] = 1

    if green_first[0] is not None:
      if blue_first[0] is not None:
        if row_diff >= 0:
            output_grid[row_diff, col_diff if col_diff is not None else 0] = 3

        else: # green is before blue
            output_grid[abs(row_diff) , abs(col_diff) ] = 3

      else:
        output_grid[0,0] = 3

    return output_grid.tolist()