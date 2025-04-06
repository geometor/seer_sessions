import copy

def transform(input_grid):
  """
  Transforms a 5x5 input grid by projecting the presence of '1's in each column
  onto the last row of the output grid. The output grid is initialized to all
  zeros. For each column in the input grid, if any cell in that column contains
  a '1', the cell in the last row (row 4) and the same column of the output
  grid is set to '1'. All other cells in the output grid remain '0'.
  """

  # Determine grid dimensions (assuming non-empty and rectangular)
  num_rows = len(input_grid)
  if num_rows == 0:
    return []
  num_cols = len(input_grid[0])
  if num_cols == 0:
    return [[] for _ in range(num_rows)] # Handle empty rows case

  # 1. Create a new output grid and initialize all its cells to 0.
  # Using list comprehension for conciseness
  output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

  # 2. For each column index `c` from 0 to num_cols - 1:
  for c in range(num_cols):
    # a. Scan the entire column `c` in the input grid.
    # b. Check if any cell in this column `c` of the input grid contains the value 1.
    found_one_in_column = False
    for r in range(num_rows):
      if input_grid[r][c] == 1:
        found_one_in_column = True
        break # Optimization: If a 1 is found, no need to check rest of the column

    # c. If at least one cell in column `c` of the input grid is 1,
    #    then set the value of the cell in the output grid at the last row
    #    (num_rows - 1) and column index `c` to 1.
    if found_one_in_column:
      # Note: row index is num_rows - 1 for the last row
      output_grid[num_rows - 1][c] = 1

  # 3. Return the modified output grid.
  return output_grid