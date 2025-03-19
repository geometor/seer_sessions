import numpy as np

def find_color_line(grid, color, orientation):
    """Finds the first line (row or column) of a given color.

    Args:
      grid: The input grid (NumPy array).
      color: The color to search for.
      orientation: 'horizontal' or 'vertical'.

    Returns:
      The index of the first row or column containing only the color, or -1 if not found.
    """
    if orientation == 'horizontal':
        for i, row in enumerate(grid):
            if np.all(row == color):
                return i
        return -1
    elif orientation == 'vertical':
        for j in range(grid.shape[1]):
            if np.all(grid[:, j] == color):
                return j
        return -1
    else:
      return -1

def find_color_column(grid, color):
    """Finds the first occurence of a column of a specified color"""
    for j in range(grid.shape[1]):
      if np.all(grid[:, j] == color):
          return j
    return -1

def find_pink_row(grid):
    """Find the horizontal line of '6' (pink) above the first all '0's row"""
    for i in range(grid.shape[0]-1):
        if np.all(grid[i,:] == 6) and np.all(grid[i+1,:]==0):
            return i;
    return -1

task = "6b6f9c7b"
train = [
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 3, 3, 3, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 3, 3, 3, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 3, 3, 3, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ], [
    [8, 8, 8, 8, 8, 8],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2],
    [0, 0, 0, 0, 2, 2],
    [0, 0, 0, 0, 0, 0],
    [4, 0, 0, 3, 3, 3],
    [4, 0, 0, 3, 3, 3],
    [4, 0, 0, 3, 3, 3],
    [4, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0]
  ]),
  ([
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 1, 0],
     [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 1, 0],
     [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 1, 0],
     [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
     [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
     [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ], [
     [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7],
     [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7],
     [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7],
     [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ], [
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0],
    [4, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0],
    [4, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0],
    [4, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ])
]

def get_boundaries(grid):
    blue_column_index = find_color_column(grid, 1)
    light_blue_row_index = find_color_line(grid, 8, 'horizontal')
    pink_row_index = find_pink_row(grid)
    yellow_column_index = find_color_column(grid, 4)
    return {
        "blue_col": blue_column_index,
        "lt_blue_row": light_blue_row_index,
        "pink_row": pink_row_index,
        "yellow_col": yellow_column_index
    }

for i, (inp, outp) in enumerate(train):
  boundaries = get_boundaries(np.array(inp))
  print(f"Example {i+1}:")
  print(f"  Boundaries: {boundaries}")
