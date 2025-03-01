import numpy as np

# Example 1 Data (from the image)
input_grid1 = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
output_grid1 = np.array([[2, 4, 1], [4, 1, 2], [1, 2, 4]])

# Previous code prediction
predicted_output1 = transform(input_grid1)
print(f"Example 1 Predicted Output:\n{predicted_output1}")
print(f"Example 1 Actual Output:\n{output_grid1}")
print(f"Example 1 Match: {np.array_equal(predicted_output1, output_grid1)}")

