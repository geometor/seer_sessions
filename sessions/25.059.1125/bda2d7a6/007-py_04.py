import numpy as np

def describe_grid(grid):
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    return {
        "rows": rows,
        "cols": cols,
        "unique_colors": unique_colors.tolist(),
        "color_counts": color_counts,
    }

def get_in_out_report(task):
    report = []
    for example in task["train"]:  # Iterate over the training examples
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        transformed_grid = transform(input_grid.copy())
        report.append({
            "input": describe_grid(input_grid),
            "output": describe_grid(output_grid),
          "transformed": describe_grid(transformed_grid),
            "match": np.array_equal(output_grid, transformed_grid)
        })
    return report
example_task = {
    "train": [
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 1, 1, 1, 5, 5, 5], [5, 5, 5, 1, 0, 1, 5, 5, 5], [5, 5, 5, 1, 1, 1, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 1, 1, 1, 5, 5, 0], [0, 5, 5, 1, 1, 1, 5, 5, 0], [0, 5, 5, 1, 1, 1, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5, 5], [5, 5, 5, 5, 5, 1, 0, 1, 5, 5, 5, 5], [5, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5, 0], [0, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5, 0], [0, 5, 5, 5, 5, 1, 1, 1, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 1, 1, 1, 5, 5], [5, 5, 1, 0, 1, 5, 5], [5, 5, 1, 1, 1, 5, 5], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5], [0, 0, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 0, 0], [5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5]]
        },
    ]
}

report = get_in_out_report(example_task)

for i, example_data in enumerate(report):
  print(f"Example {i + 1} - Match: {example_data['match']}")
  for key in example_data:
    if key != "match":
        print(f"  {key}: {example_data[key]}")
