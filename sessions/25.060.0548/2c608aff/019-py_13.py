import numpy as np

def grid_to_string(grid):
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

def analyze_differences(grid1, grid2):
    """
    Compares two grids and returns a report of the differences.
    """
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"

    diff_coords = []
    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i, j] != grid2[i, j]:
                diff_coords.append((i, j, grid1[i,j], grid2[i,j]))

    return diff_coords

def get_metrics(grid):
    """get counts of different colors, height, and width of input grid"""
    color_counts = {}
    for i in range(10):
        color_counts[i] = np.count_nonzero(grid == i)
    height = grid.shape[0]
    width = grid.shape[1]

    return color_counts, height, width

def object_metrics(grid):
    """report number of objects by size and color"""
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, count):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return count

        visited[row, col] = True
        count += 1
        count = dfs(row + 1, col, color, count)
        count = dfs(row - 1, col, color, count)
        count = dfs(row, col + 1, color, count)
        count = dfs(row, col - 1, color, count)
        return count

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                size = dfs(row, col, color, 0)
                if color not in objects:
                    objects[color] = {}
                if size not in objects[color]:
                    objects[color][size] = 0
                objects[color][size] += 1

    report = {}
    for color, sizes in objects.items():
      report[color] = []
      for size, count in sizes.items():
        report[color].append(f"{count}x{size}")
    return report

# Example usage with the first training example:
task_id = '7b601054'
examples = [
  {
    "input": [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 2, 1, 1, 1, 1], [1, 1, 1, 4, 4, 4, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]],
    "output": [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 2, 1, 1, 1, 1], [1, 1, 2, 4, 4, 4, 2, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
  },
  {
    "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 4, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]],
    "output": [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 2, 4, 2, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]]
  },
  {
    "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
    "output": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 2, 4, 4, 2, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
  },
  {
    "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 4, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]],
    "output": [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 2, 4, 2, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]]
  },
  {
    "input": [[1, 1, 1, 1, 1, 1], [1, 4, 4, 4, 4, 1], [1, 1, 1, 1, 1, 1]],
    "output": [[1, 1, 1, 1, 1, 1], [2, 4, 4, 4, 4, 2], [1, 1, 1, 1, 1, 1]]
  }
]
from pprint import pprint

for i, example in enumerate(examples):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output = transform(input_grid)

    print(f"Example {i+1}:")
    print("Input Grid:")
    pprint(grid_to_string(input_grid))
    print("\nExpected Output Grid:")
    pprint(grid_to_string(output_grid))
    print("\nPredicted Output Grid:")
    pprint(grid_to_string(predicted_output))
    print("\nDifferences (row, col, input_val, output_val):")
    diffs = analyze_differences(predicted_output, output_grid)
    pprint(diffs)

    input_metrics = get_metrics(input_grid)
    output_metrics = get_metrics(output_grid)
    print("\nInput Metrics:")
    pprint(input_metrics)
    print("\nOutput Metrics:")
    pprint(output_metrics)

    input_objects = object_metrics(input_grid)
    output_objects = object_metrics(output_grid)
    print("\nInput Objects")
    pprint(input_objects)
    print("\nOutput Objects")
    pprint(output_objects)

    print("-" * 30)
