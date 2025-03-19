import numpy as np

def count_mismatches(predicted, expected):
    """Counts the number of differing pixels between two grids."""
    return np.sum(np.array(predicted) != np.array(expected))

def analyze_results(examples):
    """Analyzes a list of examples, comparing predicted and expected outputs."""
    results = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        expected_output = example["output"]
        predicted_output = transform(input_grid)
        mismatches = count_mismatches(predicted_output, expected_output)
        results.append({
            "example": i + 1,
            "input_shape": np.array(input_grid).shape,
            "output_shape": np.array(expected_output).shape,
            "mismatches": mismatches,
            "success": mismatches == 0
        })
    return results


examples = [
    {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0], [0, 0, 0, 0, 2, 0, 2, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 8, 2, 0, 0], [0, 0, 0, 0, 8, 0, 8, 0, 0], [0, 0, 0, 0, 2, 8, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2, 0, 0], [0, 2, 0, 0, 0, 2, 0, 0], [0, 2, 0, 0, 0, 2, 0, 0], [0, 2, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 8, 8, 8, 2, 0, 0], [0, 8, 0, 0, 0, 8, 0, 0], [0, 8, 0, 0, 0, 8, 0, 0], [0, 2, 8, 8, 8, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2, 0]], 'output': [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 2, 0]]},
    {'input': [[2, 2, 2, 2, 2], [2, 0, 0, 0, 2], [2, 0, 0, 0, 2], [2, 0, 0, 0, 2], [2, 2, 2, 2, 2]], 'output': [[2, 8, 8, 8, 2], [8, 0, 0, 0, 8], [8, 0, 0, 0, 8], [8, 0, 0, 0, 8], [2, 8, 8, 8, 2]]}
]

analysis = analyze_results(examples)
print(analysis)
