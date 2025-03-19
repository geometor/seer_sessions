import numpy as np

def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform(input_grid.tolist())  # Use the provided transform function

        # Check for equality using numpy
        is_correct = np.array_equal(predicted_output, expected_output)

        # Get dimensions
        input_height, input_width = input_grid.shape
        expected_height, expected_width = expected_output.shape
        predicted_height, predicted_width = predicted_output.shape
        
        azure_row_count = 0
        for row in input_grid:
          if 8 in row:
            azure_row_count +=1

        results.append({
            'input_dims': (input_height, input_width),
            'expected_dims': (expected_height, expected_width),
            'predicted_dims': (predicted_height, predicted_width),
            'is_correct': is_correct,
            'azure_row_count': azure_row_count
        })
    return results
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8]],
            "output": [[0, 8, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 8, 0, 0, 0, 0, 0, 8, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0, 0, 0, 8]],
            "output": [[0, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0, 0, 0, 8],[0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0],[8, 0, 0, 0, 0, 0, 0, 0, 8]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 8, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[8, 8, 8, 8, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 8]]
        }
    ]
}

results = analyze_results(task)
print(results)