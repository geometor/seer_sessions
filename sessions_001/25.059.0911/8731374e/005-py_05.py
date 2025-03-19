input_grid1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 1, 1, 1],
                       [0, 0, 0, 0, 0, 1, 1, 1]])

output_grid1 = np.array([[1, 2, 1, 2, 1, 2],
                        [2, 1, 2, 1, 2, 1],
                        [1, 2, 1, 2, 1, 2]])

predicted_output1 = transform(input_grid1)

results1 = code_execution(input_grid1, output_grid1, predicted_output1)
print(results1)