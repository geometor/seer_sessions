import numpy as np

def analyze_results(examples, results):
    analysis = []
    for idx, (example, result) in enumerate(zip(examples, results)):
        input_grid, expected_output = example
        actual_output = result["output"]
        input_grid = np.array(input_grid)
        expected_output = np.array(expected_output)
        actual_output = np.array(actual_output)

        correct = np.array_equal(expected_output, actual_output)
        error_rate = 0
        if not correct:
          error_rate = np.sum(expected_output != actual_output) / expected_output.size
        
        analysis.append({
            "example_index": idx,
            "input_shape": input_grid.shape,
            "output_shape": expected_output.shape,
            "correct": correct,
            "error_rate": error_rate,
        })
    return analysis

examples = [
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 8, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], [[2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8], [2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8], [2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 8, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8], [2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8], [2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8], [2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8]]),
    ([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 8, 3, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], [[2, 8, 3, 2, 8, 3, 2], [8, 3, 2, 8, 3, 2, 8], [3, 2, 8, 3, 2, 8, 3], [2, 8, 3, 2, 8, 3, 2], [8, 3, 2, 8, 3, 2, 8], [3, 2, 8, 3, 2, 8, 3], [2, 8, 3, 2, 8, 3, 2]]),
]

previous_results = [
    {'output': [[2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8], [2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8], [2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8]]},
    {'output': [[2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8], [2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8], [2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8], [2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3], [8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2], [3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8, 3, 2, 8]]},
    {'output': [[2, 8, 3, 2, 8, 3, 2], [8, 3, 2, 8, 3, 2, 8], [3, 2, 8, 3, 2, 8, 3], [2, 8, 3, 2, 8, 3, 2], [8, 3, 2, 8, 3, 2, 8], [3, 2, 8, 3, 2, 8, 3], [2, 8, 3, 2, 8, 3, 2]]},
]

analysis = analyze_results(examples, previous_results)
print(analysis)
