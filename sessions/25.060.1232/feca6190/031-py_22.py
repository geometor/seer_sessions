import numpy as np

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        # Input Analysis
        non_zero_indices = np.nonzero(input_grid)
        non_zero_values = input_grid[non_zero_indices]
        num_non_zero = len(non_zero_values)
        input_height, input_width = input_grid.shape

        # Output Analysis
        output_height, output_width = output_grid.shape

        results.append({
            'example': i + 1,
            'input_height': input_height,
            'input_width': input_width,
            'num_non_zero': num_non_zero,
            'non_zero_values': non_zero_values.tolist(),
            'non_zero_indices_row': non_zero_indices[0].tolist(),
            'non_zero_indices_col': non_zero_indices[1].tolist(),
            'output_height': output_height,
            'output_width': output_width,
        })
    return results

# Assuming 'task' is a dictionary containing the 'train' examples
examples = [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1]], 'output': [[1]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 2, 0]], 'output': [[0, 2], [2, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 3, 0, 0]], 'output': [[0, 0, 3], [0, 3, 0], [3, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 4, 0, 0, 0]], 'output': [[0, 0, 0, 4], [0, 0, 4, 0], [0, 4, 0, 0], [4, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 5, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 5], [0, 0, 0, 5, 0], [0, 0, 5, 0, 0], [0, 5, 0, 0, 0], [5, 0, 0, 0, 0]]}
]

analysis = analyze_examples(examples)

for item in analysis:
    print(item)
