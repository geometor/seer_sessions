input_grid0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 1, 1],
                       [0, 0, 0, 0, 0, 0, 1, 1],
                       [0, 0, 0, 0, 0, 1, 1, 1]])

output_grid0 = np.array([[1, 2, 1, 2, 1, 2],
                        [2, 1, 2, 1, 2, 1],
                        [1, 2, 1, 2, 1, 2],
                        [2, 1, 2, 1, 2, 1],
                        [1, 2, 1, 2, 1, 2]])

predicted_output0 = transform(input_grid0)
results0 = code_execution(input_grid0, output_grid0, predicted_output0)
print(results0)
