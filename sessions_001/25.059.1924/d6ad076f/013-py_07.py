import numpy as np

def code_execution(input_grid, output_grid, predicted_output, error, example_index):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)

    print(f"Example {example_index + 1}:")
    print(f"  Error: {error}")

    # Find differences between the expected and predicted outputs.
    diff = np.where(output_grid != predicted_output)
    num_diffs = diff[0].size
    print(f"  Differences between expected and predicted: {num_diffs} pixels")
    if(num_diffs > 0):
        print(f"     first diff at {diff[0][0]},{diff[1][0]} output {output_grid[diff[0][0],diff[1][0]]} predicted {predicted_output[diff[0][0],diff[1][0]]}")

    rectangles = find_rectangles(input_grid)
    print(f"  Rectangles found in input: {len(rectangles)}")
    for i, rect in enumerate(rectangles):
        print(f"    Rectangle {i + 1}:")
        print(f"      Color: {rect['color']}")
        print(f"      Start: ({rect['start_row']}, {rect['start_col']})")
        print(f"      End: ({rect['end_row']}, {rect['end_col']})")

task = {
  "train": [
      {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0, 4, 4]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 8, 8, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0, 4, 4]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 0, 0, 0, 0, 0, 0], [0, 0, 3, 3, 0, 0, 0, 0, 0, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 8, 8, 8, 5, 5, 0], [7, 7, 7, 7, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
      {
      "input": [[1, 1, 0, 0, 0, 0, 0, 0, 2, 2], [1, 1, 0, 0, 0, 0, 0, 0, 2, 2]],
      "output": [[1, 1, 8, 8, 8, 8, 8, 8, 2, 2], [1, 1, 0, 0, 0, 0, 0, 0, 2, 2]]
    }
  ],
  "test": [
        {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 9, 9, 9, 9], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 9, 9, 9, 9], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0, 0, 0]]
    }
  ]
}

results = []
for i, example in enumerate(task["train"]):
  input_grid = example["input"]
  output_grid = example["output"]
  predicted_output = transform(input_grid)
  error = not np.array_equal(output_grid, predicted_output)
  results.append((input_grid, output_grid, predicted_output, error, i))
  code_execution(*results[-1])