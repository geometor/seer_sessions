# Example 3 Data
input_grid3 = np.array([[0, 5, 0, 5, 0, 5],
                      [5, 0, 5, 0, 5, 0],
                      [0, 5, 0, 5, 0, 5],
                      [5, 0, 5, 0, 5, 0],
                      [0, 5, 0, 5, 0, 5],
                      [5, 0, 5, 0, 5, 0]])
output_grid3 = np.array([[2, 4, 1, 2, 4, 1],
                       [4, 1, 2, 4, 1, 2],
                       [1, 2, 4, 1, 2, 4],
                       [2, 4, 1, 2, 4, 1],
                       [4, 1, 2, 4, 1, 2],
                       [1, 2, 4, 1, 2, 4]])

# Previous code prediction
predicted_output3 = transform(input_grid3)
print(f"Example 3 Predicted Output:\n{predicted_output3}")
print(f"Example 3 Actual Output:\n{output_grid3}")
print(f"Example 3 Match: {np.array_equal(predicted_output3, output_grid3)}")
