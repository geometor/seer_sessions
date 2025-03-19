import numpy as np

def get_grid_dimensions(grid):
    return np.array(grid).shape

def calculate_dimension_ratios(input_grid, output_grid):
    input_shape = get_grid_dimensions(input_grid)
    output_shape = get_grid_dimensions(output_grid)
    return (output_shape[0] / input_shape[0], output_shape[1] / input_shape[1])

def count_objects_by_color(grid):
    """Counts the number of contiguous objects of each color in the grid."""
    grid = np.array(grid)
    visited = np.zeros_like(grid, dtype=bool)
    color_counts = {}

    def dfs(row, col, color):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return 0
        visited[row, col] = True
        return (
            1
            + dfs(row + 1, col, color)
            + dfs(row - 1, col, color)
            + dfs(row, col + 1, color)
            + dfs(row, col - 1, color)
        )

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                if color not in color_counts:
                    color_counts[color] = 0
                dfs(row,col,color)
                color_counts[color] += 1
    return color_counts
    

task_data = {
    "train": [
        {
            "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
            "output": [
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5],
            ],
        },
        {
            "input": [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "output": [[1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[8, 0, 8, 0, 8, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[8, 0, 8, 0, 8, 0], [0, 0, 0, 0, 0, 0], [8, 0, 8, 0, 8, 0], [0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[6, 0, 0], [0, 6, 0], [0, 0, 6]],
            "output": [[6, 0, 0], [0, 6, 0], [0, 0, 6]],
        },
    ]
}

results = {}
for i, example in enumerate(task_data["train"]):
  ratios = calculate_dimension_ratios(example["input"], example["output"])
  input_objects = count_objects_by_color(example["input"])
  output_objects = count_objects_by_color(example["output"])
  results[i+1] = {
      "input_shape": get_grid_dimensions(example["input"]),
      "output_shape": get_grid_dimensions(example["output"]),
      "dimension_ratios": ratios,
      'input_objects': input_objects,
      'output_objects': output_objects
  }

print(results)