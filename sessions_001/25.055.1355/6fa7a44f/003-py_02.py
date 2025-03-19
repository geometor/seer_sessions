import numpy as np

def check_output(input_grid, expected_output):
    """
    Checks if the generated output matches the expected output.

    Args:
      input_grid: the original input grid
      expected_output:  the expected output_grid

    Returns:
      output_grid: the result of the transform function
      results: a tuple - dimension check, full equality check

    """
    output_grid = transform(input_grid)
    dimensions_check = output_grid.shape == expected_output.shape
    equality_check = np.array_equal(output_grid, expected_output)
    return output_grid, (dimensions_check, equality_check)

# Example usage (assuming train_input_0, train_output_0, etc. are defined)
examples = [
    (np.array(train_input_0), np.array(train_output_0)),
    (np.array(train_input_1), np.array(train_output_1)),
    (np.array(train_input_2), np.array(train_output_2)),

]

results = {}

for i, (input_grid, expected_output) in enumerate(examples):
  output, checks = check_output(input_grid,expected_output)
  results[f"example_{i}"] = {
      "input_shape": input_grid.shape,
      "output_shape": output.shape,
        "expected_shape": expected_output.shape,
      "dimension_check": checks[0],
      "equality_check": checks[1]
  }

print(results)
