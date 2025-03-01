import numpy as np

def get_top_row_colors(grid):
    """Returns a list of colors in the top row of the grid."""
    return grid[0, :].tolist()

def find_color_locations(grid, color):
    """Returns a list of (row, col) tuples where the specified color exists."""
    return [(r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == color]

def check_adjacency_specific(grid, r, c, color):
    """Checks if a specific cell (r, c) is adjacent to the specified color.

    Adjacency includes diagonals.
    """
    rows, cols = grid.shape
    adjacent_cells = []
    for i in range(max(0, r - 1), min(rows, r + 2)):
        for j in range(max(0, c - 1), min(cols, c + 2)):
            if (i, j) != (r, c):  # Exclude the cell itself
                adjacent_cells.append(grid[i,j])
    return color in adjacent_cells

def check_horizontal_mirror(grid):
  return np.array_equal(grid, np.fliplr(grid))

def check_vertical_mirror(grid):
  return np.array_equal(grid, np.flipud(grid))

def check_full_mirror(grid):
  return np.array_equal(grid, np.flipud(np.fliplr(grid)))

def transform(input_grid):
    """Applies the hypothesized transformation rule."""
    output_grid = input_grid.copy()
    blue_locations = find_color_locations(input_grid, 1)
    for r, c in blue_locations:
        if check_adjacency_specific(input_grid, r, c, 0):
            output_grid[r, c] = 2
    return output_grid

task_data = {
    'train': {
        'input': [
            [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
            [[0, 0, 0, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]],
            [[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]
        ],
        'output': [
            [[0, 2, 0], [0, 2, 0], [0, 2, 0]],
            [[0, 0, 0, 2, 0], [0, 0, 0, 2, 0], [0, 0, 0, 0, 0]],
            [[0, 0, 2, 0, 0], [0, 0, 2, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0]]
        ]
    }
}

input_grids = task_data['train']['input']
output_grids = task_data['train']['output']
results = []

for i in range(len(input_grids)):
  input_grid = np.array(input_grids[i])
  output_grid = np.array(output_grids[i])
  transformed_grid = transform(input_grid)
  results.append(np.array_equal(transformed_grid, output_grid))

print(results)