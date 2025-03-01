import numpy as np

def examine_example(input_grid, expected_output, transform_output):
    input_dims = input_grid.shape
    output_dims = expected_output.shape
    
    # Check for 2x2 repetition
    repetition_check = True
    if output_dims[0] >= 2 * input_dims[0] and output_dims[1] >= 2 * input_dims[1]:
        for i in range(2):
            for j in range(2):
                if not np.array_equal(input_grid, expected_output[i*input_dims[0]:(i+1)*input_dims[0], j*input_dims[1]:(j+1)*input_dims[1]]):
                    repetition_check = False
                    break
            if not repetition_check:
                break
    else:
        repetition_check = False

    # Find fill values (cells outside of the repeated blocks). Simplified for demonstration; might need refinement.
    fill_values = []
    if repetition_check:  # Only check fill if repetition is present.
        for r in range(output_dims[0]):
            for c in range(output_dims[1]):
              if r >= input_dims[0] and r < input_dims[0] * 2:
                if c >= input_dims[1] and c< input_dims[1] *2:
                  continue #skip, inside repetition
              fill_values.append(expected_output[r,c])
    
    # Identify mismatched pixels
    mismatched_pixels = []
    for row in range(output_dims[0]):
        for col in range(output_dims[1]):
            if transform_output[row, col] != expected_output[row, col]:
                mismatched_pixels.append(((row, col), transform_output[row, col], expected_output[row, col]))

    return {
        "input_dims": input_dims,
        "output_dims": output_dims,
        "repetition_check": repetition_check,
        "fill_values": list(np.unique(fill_values)),
        "mismatched_pixels": mismatched_pixels,
    }

# Example Usage with provided data:
#train1
input_grid1 = np.array([[8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8],
                        [8, 8, 8, 1, 8],
                        [8, 8, 8, 8, 8]])
output_grid1 = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 8, 1, 8, 8, 8, 8, 1, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 8, 1, 8, 8, 8, 8, 1, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
transform_output1 = transform(input_grid1)
result1 = examine_example(input_grid1, output_grid1, transform_output1)
print(f"Example 1 Results: {result1}")

#train2
input_grid2 = np.array([[8, 8, 8, 8, 8, 8, 8, 8],
                        [8, 8, 7, 8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8, 8, 8, 8],
                        [8, 8, 7, 8, 8, 7, 8, 8],
                        [8, 8, 8, 8, 8, 8, 8, 8],
                        [8, 8, 8, 8, 8, 8, 7, 8],
                        [8, 8, 8, 8, 8, 8, 8, 8]])
output_grid2 = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 7, 8, 8, 8, 8, 8, 8, 8, 7, 8, 8, 8, 8, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 7, 8, 8, 7, 8, 8, 8, 8, 7, 8, 8, 7, 8, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 8, 8, 8, 8, 7, 8, 8, 8, 8, 8, 8, 8, 7, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 7, 8, 8, 7, 8, 8, 8, 8, 7, 8, 8, 7, 8, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                         [8, 8, 8, 8, 8, 8, 7, 8, 8, 8, 8, 8, 8, 8, 7, 8],
                         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
transform_output2 = transform(input_grid2)
result2 = examine_example(input_grid2, output_grid2, transform_output2)
print(f"Example 2 Results: {result2}")

#train3
input_grid3 = np.array([[2, 0, 2, 0, 2, 0, 2],
                        [0, 2, 0, 2, 0, 2, 0],
                        [2, 0, 2, 0, 2, 0, 2],
                        [0, 2, 0, 2, 0, 2, 0],
                        [2, 0, 2, 0, 2, 0, 2],
                        [0, 2, 0, 2, 0, 2, 0],
                        [2, 0, 2, 0, 2, 0, 2]])
output_grid3 = np.array([[2, 0, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 0, 2],
                         [0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0],
                         [2, 0, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 0, 2],
                         [0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0],
                         [2, 0, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 0, 2],
                         [0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0],
                         [2, 0, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 0, 2],
                         [2, 0, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 0, 2],
                         [0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0],
                         [2, 0, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 0, 2],
                         [0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0],
                         [2, 0, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 0, 2],
                         [0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0],
                         [2, 0, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 0, 2]])
transform_output3 = transform(input_grid3)
result3 = examine_example(input_grid3, output_grid3, transform_output3)
print(f"Example 3 Results: {result3}")