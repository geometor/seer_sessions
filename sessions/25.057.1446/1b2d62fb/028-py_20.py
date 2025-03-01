import numpy as np

# Example Grids (replace with actual data from the task)
examples = [
    {
        "input": np.array([[0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0]]),
        "output": np.array([[0, 8, 0],
                            [0, 8, 0],
                            [0, 8, 0]])
    },
    {
        "input": np.array([[0, 0, 1, 0, 0, 0, 0],
                           [0, 0, 1, 0, 5, 0, 0],
                           [0, 0, 1, 0, 0, 0, 0]]),
        "output": np.array([[0, 8, 0],
                            [0, 8, 0],
                            [0, 8, 0]])

    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 1, 5, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0],
                            [0, 8, 8],
                            [0, 0, 0]])

    },
    {
        "input": np.array([[0, 1, 0, 0, 0, 0, 0],
                           [0, 1, 0, 0, 5, 0, 0],
                           [0, 1, 0, 0, 0, 1, 0]]),
        "output": np.array([[0, 8, 0],
                            [0, 8, 0],
                            [0, 8, 0]])
    }
]

def analyze_examples_detailed(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        expected_output = example["output"]

        # Find columns with '1' (blue)
        columns_with_blue = np.where(np.any(input_grid == 1, axis=0))[0]
        
        # Find rows that have any non-zero values
        rows_with_non_zero = np.where(np.any(input_grid != 0, axis=1))[0]

        #Determine expected output width
        expected_width = 0
        if len(columns_with_blue) > 0:
            expected_width = 3  #default to center column selected

        results.append({
            "example_index": i,
            "input_shape": input_grid.shape,
            "output_shape": expected_output.shape,
            "columns_with_blue": columns_with_blue.tolist(),
            "rows_with_non_zero": rows_with_non_zero.tolist(),
            "expected_width": expected_width
        })
    return results
analysis_results = analyze_examples_detailed(examples)

for result in analysis_results:
    print(result)
