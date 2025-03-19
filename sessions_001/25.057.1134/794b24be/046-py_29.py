import numpy as np

# Example data (replace with actual data from the task)
# Input grids for examples 1 to 3
input_grids = [
    np.array([[0, 0, 0], [0, 0, 0], [0, 1, 0]]),  # Example 1 Input
    np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]]),  # Example 2 Input
    np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]]),  # Example 3 Input
]

# Expected output grids for examples 1 to 3
expected_output_grids = [
    np.array([[0, 0, 0], [0, 0, 0], [0, 2, 0]]),  # Example 1 Output
    np.array([[0, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 0]]),  # Example 2 Output
    np.array([[0, 2, 0], [0, 2, 0], [0, 2, 0]]),  # Example 3 Output
]

# output from previous step
transformed_grids = [
    np.array([[0, 0, 0], [0, 0, 0], [0, 2, 0]]),  # Example 1 Transformed
    np.array([[0, 0, 0, 0], [0, 2, 2, 0], [0, 0, 0, 0]]),  # Example 2 Transformed
    np.array([[0, 0, 0], [0, 2, 0], [0, 2, 0]]),  # Example 3 Transformed
]

# Compare transformed grids with expected outputs
comparison_results = []
for i in range(len(expected_output_grids)):
    comparison = transformed_grids[i] == expected_output_grids[i]
    comparison_results.append(comparison)
    print(f"Example {i+1} Comparison (Transformed == Expected):\n{comparison}\n")
    mismatches = np.where(comparison == False)
    if len(mismatches[0]) > 0:
      print(f"Mismatched indices (row, col): {list(zip(mismatches[0], mismatches[1]))}")
      for row, col in zip(mismatches[0], mismatches[1]):
          print(
              f"  - At ({row}, {col}): Transformed={transformed_grids[i][row, col]}, Expected={expected_output_grids[i][row, col]}"
          )
    else:
      print("No mismatches")
    print("-" * 20)
