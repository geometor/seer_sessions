# Example 2 Data
input_grid2 = np.array([[0, 3, 0, 3, 0],
                      [3, 0, 3, 0, 3],
                      [0, 3, 0, 3, 0],
                      [3, 0, 3, 0, 3],
                      [0, 3, 0, 3, 0]])
output_grid2 = np.array([[2, 4, 1, 2, 4],
                       [4, 1, 2, 4, 1],
                       [1, 2, 4, 1, 2],
                       [2, 4, 1, 2, 4],
                       [4, 1, 2, 4, 1]])

# Previous code prediction
predicted_output2 = transform(input_grid2)
print(f"Example 2 Predicted Output:\n{predicted_output2}")
print(f"Example 2 Actual Output:\n{output_grid2}")
print(f"Example 2 Match: {np.array_equal(predicted_output2, output_grid2)}")