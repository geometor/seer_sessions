def get_object_coords(grid, color):
    """Returns a list of (row, col) coordinates for the given color."""
    return list(zip(*np.where(grid == color)))

def get_adjacent_coords(grid, coord):
    r, c = coord
    rows, cols = grid.shape
    adjacent = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            adjacent.append((nr, nc))
    return adjacent

def analyze_example(input_grid, output_grid):
    azure_coords_in = get_object_coords(input_grid, 8)
    azure_coords_out = get_object_coords(output_grid, 8)
    red_coords_out = get_object_coords(output_grid, 2)

    print(f"Input Azure Coords: {azure_coords_in}")
    print(f"Output Azure Coords: {azure_coords_out}")
    print(f"Output Red Coords: {red_coords_out}")

    for coord in azure_coords_in:
      adj_in = get_adjacent_coords(input_grid, coord)
      print(f"adj_in: {coord} : {adj_in}")
    for coord in azure_coords_out:
      adj_out = get_adjacent_coords(output_grid, coord)
      print(f"adj_out: {coord} : {adj_out}")
    for coord in red_coords_out:
      adj_red = get_adjacent_coords(output_grid, coord)
      print(f"adj_red: {coord} : {adj_red}")

import numpy as np
#task.train[0].input_grid
#task.train[0].output_grid
#task.train[1].input_grid
#task.train[1].output_grid
#task.train[2].input_grid
task = task.train[2].output_grid

analyze_example(task.train[2].input_grid, task)
#analyze_example(task.train[1].input_grid, task.train[1].output_grid)
#analyze_example(task.train[2].input_grid, task.train[2].output_grid)
