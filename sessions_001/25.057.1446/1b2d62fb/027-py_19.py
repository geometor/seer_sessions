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
                            [0, 8, 0],
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

def analyze_examples(examples, transform_func):
    results = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        expected_output = example["output"]
        predicted_output = transform_func(input_grid)
        
        # Find columns with '1' (blue)
        columns_with_blue = np.where(np.any(input_grid == 1, axis=0))[0]

        results.append({
            "example_index": i,
            "input_shape": input_grid.shape,
            "output_shape": predicted_output.shape,
            "expected_output_shape": expected_output.shape,
            "columns_with_blue": columns_with_blue.tolist(),
            "predicted_output": predicted_output.tolist(),
            "expected_output": expected_output.tolist(),
            "match": np.array_equal(predicted_output, expected_output)
        })
    return results

previous_transform = transform # renamed for clarity in output

analysis_results = analyze_examples(examples, previous_transform)

for result in analysis_results:
    print(result)