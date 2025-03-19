import numpy as np

def get_red_pixel_mapping(input_grid, output_grid):
    """
    Analyzes the mapping of red pixels from input to output grid.

    Returns:
        A dictionary where keys are (input_row, input_col) of red pixels
        and values are corresponding (output_row, output_col) or None if not mapped.
    """
    red_pixel_mapping = {}
    red_pixels_input = np.argwhere(input_grid == 2)

    scale_row = input_grid.shape[0] / 3
    scale_col = input_grid.shape[1] / 3

    for r_in, c_in in red_pixels_input:
      r_out = int(r_in / scale_row)
      if r_out > 2: r_out = 2
      c_out = int(c_in / scale_col)
      if c_out > 2: c_out = 2
      if output_grid[r_out, c_out] == 2:
          red_pixel_mapping[(r_in, c_in)] = (r_out, c_out)

    return red_pixel_mapping
def calculate_centroid(coordinates):
    """Calculates the centroid of a list of (row, col) coordinates."""
    if not coordinates:
        return None
    return (
      sum([c[0] for c in coordinates]) / len(coordinates),
      sum([c[1] for c in coordinates]) / len(coordinates)
      )
def find_connected_components(input_grid):
  """
    find the connected components, limit search to 8 connectivity, diagonals are
    connections
  """
  visited = set()
  components = []

  def dfs(row, col, current_component):
    if (
        row < 0
        or row >= input_grid.shape[0]
        or col < 0
        or col >= input_grid.shape[1]
        or (row, col) in visited
        or input_grid[row, col] != 2
    ):
      return

    visited.add((row, col))
    current_component.append((row, col))

    # Explore all 8 neighbors (including diagonals)
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        if dr == 0 and dc == 0:
          continue
        dfs(row + dr, col + dc, current_component)


  for row in range(input_grid.shape[0]):
      for col in range(input_grid.shape[1]):
          if input_grid[row, col] == 2 and (row, col) not in visited:
              current_component = []
              dfs(row, col, current_component)
              components.append(current_component)
  return components

def analyze_training_pairs(task):
    print(f"Task: {task['id']}")
    for i, example in enumerate(task['train']):
      input_grid = np.array(example['input'])
      output_grid = np.array(example['output'])
      print(f"  Example {i+1}:")

      mapping = get_red_pixel_mapping(input_grid, output_grid)
      print(f"    Red Pixel Mapping: {mapping}")
      components = find_connected_components(input_grid)
      print(f"    connected components {components}")
      centroids = [calculate_centroid(component) for component in components]
      print(f"    Centroids of components: {centroids}")

from json_data import tasks
for task in tasks:
  if task['id'] == "6b16e72d":
    analyze_training_pairs(task)

