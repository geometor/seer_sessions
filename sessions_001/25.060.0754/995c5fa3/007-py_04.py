import numpy as np
from collections import Counter

def describe_grid(grid):
    shape = grid.shape
    unique_colors = Counter(grid.flatten())
    color_counts = {color: count for color, count in unique_colors.items()}
    return shape, color_counts

task_data = {
    "train": [
        {
            "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
            "output": [[2, 2, 2], [8, 8, 8], [3, 3, 3]]
        },
        {
            "input": [[7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7], [7, 7, 7, 7]],
            "output": [[2, 2, 2], [8, 8, 8], [3, 3, 3]]
        },
		{
            "input": [[6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6]],
            "output": [[2, 2, 2], [8, 8, 8], [3, 3, 3]]
        },
		{
            "input": [[1]],
            "output": [[2, 2, 2], [8, 8, 8], [3, 3, 3]]
        }
    ]
}

results = []
for example in task_data["train"]:
  input_grid = np.array(example["input"])
  output_grid = np.array(example["output"])
  input_shape, input_colors = describe_grid(input_grid)
  output_shape, output_colors = describe_grid(output_grid)

  # call transform function
  transformed_grid = transform(input_grid)

  # check equality
  grids_equal = np.array_equal(output_grid, transformed_grid)


  results.append(
        {
            "input_shape": input_shape,
            "input_colors": input_colors,
            "output_shape": output_shape,
            "output_colors": output_colors,
            "grids_equal": grids_equal
        }
    )

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Input Colors: {result['input_colors']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Output Colors: {result['output_colors']}")
    print(f"  Grids Equal: {result['grids_equal']}")
    print("-" * 20)