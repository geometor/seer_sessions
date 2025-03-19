import numpy as np

def analyze_examples(task):
    results = []
    for example in task["train"]:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        actual_output = np.array(transform(example['input']))
        
        rows, cols = input_grid.shape
        blue_col = find_blue_column(input_grid)

        discrepancy = not np.array_equal(expected_output, actual_output)

        
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': expected_output.shape,
            'blue_column': blue_col,
            'discrepancy': discrepancy,
            'input': input_grid.tolist(),
            'expected': expected_output.tolist(),
            'actual': actual_output.tolist()
        })
    return results

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 1, 5, 0, 0], [0, 5, 5, 5, 5, 5, 1, 5, 0, 0], [0, 5, 5, 5, 5, 5, 1, 5, 0, 0], [0, 5, 5, 5, 5, 5, 1, 5, 0, 0], [0, 5, 5, 5, 5, 5, 1, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 5, 0], [0, 5, 0], [0, 5, 0], [0, 5, 0], [0, 5, 0], [0, 5, 0], [0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 5, 5, 1, 0], [0, 5, 5, 5, 5, 5, 5, 5, 1, 0], [0, 5, 5, 5, 5, 5, 5, 5, 1, 0], [0, 5, 5, 5, 5, 5, 5, 5, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 1, 5, 0, 0], [0, 5, 5, 5, 5, 5, 1, 5, 0, 0], [0, 5, 5, 5, 5, 5, 1, 5, 0, 0], [0, 5, 5, 5, 5, 5, 1, 5, 0, 0], [0, 5, 5, 5, 5, 5, 1, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 5, 0], [0, 5, 0], [0, 5, 0], [0, 5, 0], [0, 5, 0], [0, 5, 0], [0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 0], [0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 0], [0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 0], [0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0], [0, 7, 0], [0, 7, 0], [0, 7, 0], [0, 7, 0], [0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0], [0, 8, 0], [0, 8, 0], [0, 8, 0], [0, 8, 0], [0, 8, 0], [0, 0, 0]],
        },
    ]
}

analysis = analyze_examples(task)
for result in analysis:
    print(result)