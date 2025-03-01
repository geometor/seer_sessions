def calculate_accuracy(input_grid, expected_output, actual_output):
    """Calculates the accuracy of the transformation."""
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    if expected_output.shape != actual_output.shape:
        return f"Dimension mismatch: Expected {expected_output.shape}, Actual {actual_output.shape}"

    correct_pixels = np.sum(expected_output == actual_output)
    total_pixels = expected_output.size  # Use .size for total number of elements
    accuracy = (correct_pixels / total_pixels) * 100 if total_pixels >0 else 0
    return accuracy, correct_pixels, total_pixels

def get_grid_dimensions(grid):
   grid = np.array(grid)
   return grid.shape

examples = [
    {
        "input": [
            [5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5],
            [5, 5, 4, 4, 5, 5],
            [5, 5, 4, 4, 5, 5],
            [5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5]
        ],
        "output": [
            [5, 5, 5],
            [5, 3, 5],
            [5, 5, 5]
        ]
    },
    {
        "input": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 4, 4, 5, 5, 5, 5],
            [5, 5, 5, 5, 4, 4, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        ],
        "output": [
            [5, 5, 5, 5, 5],
            [5, 5, 3, 5, 5],
            [5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5]
        ]
    },
    {
      "input":  [
            [5, 5, 5, 5, 5],
            [5, 5, 5, 4, 5],
            [5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5],
            [5, 5, 5, 5, 1]
],
        "output": [
            [5, 5, 5],
            [5, 5, 5],
            [5, 5, 1]
        ]
    }
]

for i, example in enumerate(examples):
  input_grid = example["input"]
  expected_output = example["output"]
  actual_output = transform(input_grid)
  accuracy, correct_pixels, total_pixels = calculate_accuracy(input_grid, expected_output, actual_output)
  input_dims = get_grid_dimensions(input_grid)
  output_dims = get_grid_dimensions(expected_output)
  print (f"example: {i}")
  print(f"input dims: {input_dims}")
  print(f"output dims: {output_dims}")
  print(f"accuracy: {accuracy}")
  print(f"correct pixels: {correct_pixels}")
  print(f"total pixels: {total_pixels}")
  print("---")