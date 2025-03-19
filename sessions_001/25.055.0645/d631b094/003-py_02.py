import numpy as np

def count_blue_pixels(grid):
    """Counts the number of blue pixels (value 1) in a grid."""
    count = 0
    for row in grid:
        for pixel in row:
            if pixel == 1:
                count += 1
    return count

def transform(input_grid):
    """Transforms the input grid into the output grid."""

    # Count blue pixels in the input grid.
    blue_count = count_blue_pixels(input_grid)

    # Create output grid: 1 x blue_count, filled with blue (1s).
    output_grid = np.ones((1, blue_count), dtype=int)

    return output_grid

def show_grid(grid_data, label=""):
    print(f"== {label} ==")
    if isinstance(grid_data, list):
        grid = np.array(grid_data)
    else:
        grid = grid_data
    for row in grid:
        print("".join(map(str, row)))

task = {
    "train": [
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[1, 1, 1]]
        },
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[1, 1, 1]]
        },
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 0, 0, 0, 8, 8], [8, 8, 8, 8, 8, 8, 0, 0, 0, 8, 8], [8, 8, 8, 8, 8, 8, 0, 0, 0, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[1, 1, 1]]
        },
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[1, 1, 1]]
        }
    ],
    "test": [
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8, 8], [8, 8, 8, 0, 0, 0, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[1, 1, 1]]
        }
    ]
}

for example_index, example in enumerate(task["train"]):
  input_grid = example["input"]
  expected_output = example["output"]
  actual_output = transform(np.array(input_grid))
  show_grid(input_grid, label=f"Example {example_index + 1} - Input")
  show_grid(expected_output, label=f"Example {example_index + 1} - Expected Output")
  show_grid(actual_output, label=f"Example {example_index + 1} - Actual Output")

  if np.array_equal(actual_output, np.array(expected_output)):
    print("Result: PASS")
  else:
      print("Result: FAIL")
  print("-" * 20)