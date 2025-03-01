input_grid2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 1]])
output_grid2 = np.array([[1, 2, 1, 2, 1, 2],
                        [2, 1, 2, 1, 2, 1],
                        [1, 2, 1, 2, 1, 2]])
predicted_output2 = transform(input_grid2)

results2 = code_execution(input_grid2, output_grid2, predicted_output2)
print(results2)