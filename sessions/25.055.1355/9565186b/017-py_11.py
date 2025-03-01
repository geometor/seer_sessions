import numpy as np

def analyze_results(examples):
    results = []
    for i, (input_grid, output_grid) in enumerate(examples):
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)

        #check for identical match
        identical = np.array_equal(input_grid, output_grid)

        # Find where the input and output grids differ
        diff_indices = np.where(input_grid != output_grid)

        # Get the values at the differing indices
        input_values_at_diff = input_grid[diff_indices]
        output_values_at_diff = output_grid[diff_indices]
        
        #number of azure in input
        num_azure_input = np.count_nonzero(input_grid == 8)
        num_gray_input = np.count_nonzero(input_grid == 5)
        
        #number of azure in output
        num_azure_output = np.count_nonzero(output_grid == 8)
        num_gray_output = np.count_nonzero(output_grid == 5)
        
        results.append(
            {
                "example": i + 1,
                "identical": identical,
                "diff_indices": diff_indices,
                "input_values_at_diff": input_values_at_diff.tolist(),
                "output_values_at_diff": output_values_at_diff.tolist(),
                "num_azure_input": num_azure_input,
                "num_gray_input": num_gray_input,
                "num_azure_output": num_azure_output,
                "num_gray_output": num_gray_output,
            }
        )
    return results
#the training examples used for the previous code
examples = [
    ([[8, 1, 3, 8, 8], [8, 8, 8, 8, 8], [8, 8, 8, 8, 8], [8, 8, 8, 1, 8]], [[5, 1, 3, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 1, 5]]),
    ([[8, 7, 8, 7], [6, 8, 7, 8], [8, 7, 8, 6], [7, 8, 6, 8]], [[5, 7, 5, 7], [6, 5, 7, 5], [5, 7, 5, 6], [7, 5, 6, 5]]),
    ([[0, 8, 0, 8, 8, 8], [8, 8, 0, 0, 8, 8], [8, 8, 8, 8, 0, 0]], [[0, 5, 0, 5, 5, 5], [5, 5, 0, 0, 5, 5], [5, 5, 5, 5, 0, 0]]),
]
analysis_results = analyze_results(examples)

for result in analysis_results:
    print(result)