import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    print("Input Grid:")
    print(input_grid)
    print("Expected Output Grid:")
    print(output_grid)
    print("Predicted Output Grid:")
    print(predicted_grid)

    # Find differences between predicted and expected outputs
    diff = output_grid != predicted_grid
    print(f"\nDifferences Exist: {np.any(diff)}")
    if np.any(diff):
      print("\nDifference Locations (row, col):")
      diff_rows, diff_cols = np.where(diff)
      for r, c in zip(diff_rows, diff_cols):
        print(f"({r}, {c}) - Expected: {output_grid[r, c]}, Predicted: {predicted_grid[r, c]}")

    for color in range(10):  # Check all colors
        input_locations = np.where(input_grid == color)
        output_locations = np.where(output_grid == color)
        predicted_locations = np.where(predicted_grid == color)

        if input_locations[0].size > 0:  # Check if color exists in input
            print(f"\nColor {color} in Input - Locations (row, col):")
            for r, c in zip(input_locations[0], input_locations[1]):
                print(f"({r}, {c})")

        if output_locations[0].size > 0:  # Check if color exists in output
            print(f"\nColor {color} in Expected Output - Locations (row, col):")
            for r, c in zip(output_locations[0], output_locations[1]):
                print(f"({r}, {c})")
        if predicted_locations[0].size > 0:
            print(f"\nColor {color} in Predicted Output - Locations (row, col):")
            for r,c in zip(predicted_locations[0], predicted_locations[1]):
                print(f"({r}, {c})")
                

# Load the example data (replace with your actual data loading)
task_data = [
  ([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 4, 1, 2, 1, 4, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
  ], [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 4, 4, 0, 0],
    [0, 0, 4, 1, 4, 0, 0],
    [0, 4, 1, 1, 1, 4, 0],
    [0, 0, 4, 1, 4, 0, 0],
    [0, 0, 4, 4, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 4, 1, 2, 1, 4, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
  ], [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 4, 1, 1, 1, 4, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
  ]),
  ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 4, 1, 2, 1, 2, 1, 4],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  ], [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 1, 1, 1, 1, 1, 4],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  ]),
]

import json
with open("6855a6e4.json") as f:
    task = json.load(f)

train_examples = task['train']

# Example usage with your data
for i, example in enumerate(train_examples):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_grid = transform(input_grid.copy())
    print(f"--- Example {i + 1} ---")
    analyze_example(input_grid, output_grid, predicted_grid)
    print("\n\n")
