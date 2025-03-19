import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Replace all 5s with 0s.
    output_grid[output_grid == 5] = 0

    return output_grid

def analyze_example(example):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    transformed_grid = transform(input_grid)
    correct = np.array_equal(transformed_grid, output_grid)

    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    transformed_colors = np.unique(transformed_grid)

    print(f"  Input colors: {input_colors}")
    print(f"  Output colors: {output_colors}")
    print(f"  Transformed colors: {transformed_colors}")
    print(f"  Correct: {correct}")

    if not correct:
      diff = transformed_grid != output_grid
      print(f"  Differences at indices: {np.where(diff)}")
      print(f"    Transformed values: {transformed_grid[diff]}")
      print(f"    Expected values: {output_grid[diff]}")
    print("-" * 20)

examples = [
    {
        "input": [[5, 1, 1], [1, 5, 1], [1, 1, 5]],
        "output": [[0, 1, 1], [1, 0, 1], [1, 1, 0]],
    },
    {
        "input": [[5, 1, 1, 5, 1], [1, 5, 1, 1, 5]],
        "output": [[0, 1, 1, 0, 1], [1, 0, 1, 1, 0]],
    },
    {
        "input": [[1, 5, 1, 5, 1], [5, 1, 5, 1, 5], [1, 5, 1, 5, 1]],
        "output": [[1, 0, 1, 0, 1], [0, 1, 0, 1, 0], [1, 0, 1, 0, 1]],
    },
    {
        "input": [[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
        "output": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    },
    {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
    },
]

for i, example in enumerate(examples):
    print(f"Example {i + 1}:")
    analyze_example(example)
