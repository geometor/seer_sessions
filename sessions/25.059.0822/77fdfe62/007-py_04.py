import numpy as np

def describe_grid(grid, grid_name="Grid"):
    """Provides a description of a NumPy grid."""

    print(f"{grid_name}:")
    print(f"  Shape: {grid.shape}")
    unique_values = np.unique(grid)
    print(f"  Unique values: {unique_values}")
    if grid.size > 0:  # prevent errors with empty array
      for value in unique_values:
          count = np.count_nonzero(grid == value)
          print(f"  Count of {value}: {count}")
    else:
      print("grid is empty")

def evaluate_result(input_grid, expected_output, generated_output):
    """Evaluates the generated output against the expected output."""

    print("Input Grid:")
    describe_grid(input_grid)

    print("\nExpected Output:")
    describe_grid(expected_output)

    print("\nGenerated Output:")
    describe_grid(generated_output)

    print("\nComparison:")
    if generated_output.shape == expected_output.shape:
        print("  Shapes match.")
        if np.array_equal(generated_output, expected_output):
            print("  Values match. Success!")
        else:
            print("  Values do not match. Failure.")
    else:
        print("  Shapes do not match. Failure.")
    print("-" * 30)
# Example usage with a hypothetical training example
# I am commenting this out since it will change for each example
# input_grid = np.array([[1, 1, 0], [1, 1, 0], [0, 0, 2]])
# expected_output = np.array([[1, 2]])
# generated_output = transform(input_grid.copy())
# evaluate_result(input_grid, expected_output, generated_output)
