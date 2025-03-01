import numpy as np

def code_execution(input_grid, output_grid, predicted_output_grid):
    input_array = np.array(input_grid)
    output_array = np.array(output_grid)
    predicted_output_array = np.array(predicted_output_grid)

    print(f"Input shape: {input_array.shape}")
    print(f"Output shape: {output_array.shape}")
    print(f"Predicted output shape: {predicted_output_array.shape}")
    print(f"Correct output: \n{output_array}")
    print(f"Predicted output: \n{predicted_output_array}")    
    print(f"Are output and predicted output the same? {np.array_equal(output_array, predicted_output_array)}")
    print("-" * 20)

# Example 1
input1 = [[5, 5, 5, 1, 1, 1, 2, 2, 2], [5, 5, 5, 1, 1, 1, 2, 2, 2], [5, 5, 5, 1, 1, 1, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 5, 5, 1, 1, 1, 2, 2, 2], [5, 5, 5, 1, 1, 1, 2, 2, 2], [5, 5, 5, 1, 1, 1, 2, 2, 2],[5, 5, 5, 1, 1, 1, 2, 2, 2]]
output1 = [[5, 1, 2], [5, 1, 2]]
predicted_output1 = transform(np.array(input1))
code_execution(input1, output1, predicted_output1)

# Example 2
input2 = [[8, 8, 8, 8, 3, 3, 3, 3], [8, 8, 8, 8, 3, 3, 3, 3], [8, 8, 8, 8, 3, 3, 3, 3], [8, 8, 8, 8, 3, 3, 3, 3], [8, 8, 8, 8, 3, 3, 3, 3], [4, 4, 4, 4, 6, 6, 6, 6], [4, 4, 4, 4, 6, 6, 6, 6], [4, 4, 4, 4, 6, 6, 6, 6], [4, 4, 4, 4, 6, 6, 6, 6], [4, 4, 4, 4, 6, 6, 6, 6]]
output2 = [[8, 3], [4, 6]]
predicted_output2 = transform(np.array(input2))
code_execution(input2, output2, predicted_output2)

# Example 3
input3 = [[7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1]]
output3 = [[7, 0], [2, 1]]
predicted_output3 = transform(np.array(input3))
code_execution(input3, output3, predicted_output3)

# Example 4
input4 = [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
output4 = [[3]]
predicted_output4 = transform(np.array(input4))
code_execution(input4, output4, predicted_output4)