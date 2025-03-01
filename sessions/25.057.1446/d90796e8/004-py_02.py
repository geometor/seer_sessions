"""
1.  **Examine Top Row:** Inspect the top row of the input grid.
2.  **Locate Non-Zero:** Identify any non-zero numbers within the top row, noting their positions and values.
3. **If 2 Non-Zero Elements**: add them together
4.  **Calculate Result:** If there are non-zero numbers in top row, multiply the *first* non-zero number by 2, unless a sum has occurred. If there are *no* non-zero numbers, the result is 0.
5.  **Replace First Non-Zero:** In the top row, replace the first non-zero number encountered (scanning from left to right) with the calculated result.
6.  **Clear Others:** Set all *other* non-zero numbers in the top row to 0.
7.  **Preserve Rest:** All other rows in the grid remain unchanged.
8.  **Output:** The modified grid is the final output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify non-zero numbers in the top row
    top_row_numbers = []
    for j in range(cols):
        if output_grid[0, j] != 0:
            top_row_numbers.append((0, j, output_grid[0, j]))

    # Calculate result based on the number of non-zero elements
    if len(top_row_numbers) == 0:
        result = 0  # No non-zero elements
    elif len(top_row_numbers) >= 2:
      result = top_row_numbers[0][2] + top_row_numbers[1][2] #add the two numbers
      first_non_zero_index = top_row_numbers[0][1]
    else:
        result = top_row_numbers[0][2] * 2  # One non-zero element
        first_non_zero_index = top_row_numbers[0][1]
    # Replace the first non-zero element
    if len(top_row_numbers) >0:
      output_grid[0, first_non_zero_index] = result

    # Clear other non-zero elements in the top row
    for j in range(cols):
      if output_grid[0,j] != 0 and j != first_non_zero_index:
           output_grid[0,j] = 0


    return output_grid