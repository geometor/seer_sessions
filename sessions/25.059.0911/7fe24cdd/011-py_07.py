import numpy as np

def describe_grid(grid):
    """Provides a basic description of a grid."""
    return f"Shape: {grid.shape}, Colors: {np.unique(grid)}"

def analyze_example(input_grid, expected_output_grid, predicted_output_grid):
   
    print(f"Input: {describe_grid(input_grid)}")
    print(f"Expected Output: {describe_grid(expected_output_grid)}")
    print(f"Predicted Output: {describe_grid(predicted_output_grid)}")
    print(f"Prediction Correct: {np.array_equal(expected_output_grid, predicted_output_grid)}")

#Example Usage with the provided test data
input_0 = np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]])
output_0 = np.array([[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5]])
predicted_0 = transform(input_0)
analyze_example(input_0, output_0, predicted_0)

input_1 = np.array([[8, 8, 8], [8, 1, 8], [8, 8, 8]])
output_1 = np.array([[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 1, 1, 8, 8], [8, 8, 1, 1, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8]])
predicted_1 = transform(input_1)
analyze_example(input_1, output_1, predicted_1)

input_2 = np.array([[7, 0, 7], [0, 7, 0], [7, 0, 7]])
output_2 = np.array([[7, 7, 0, 0, 7, 7], [7, 7, 0, 0, 7, 7], [0, 0, 7, 7, 0, 0], [0, 0, 7, 7, 0, 0], [7, 7, 0, 0, 7, 7], [7, 7, 0, 0, 7, 7]])
predicted_2 = transform(input_2)
analyze_example(input_2, output_2, predicted_2)
