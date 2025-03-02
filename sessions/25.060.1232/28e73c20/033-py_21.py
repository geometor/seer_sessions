import numpy as np

def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)  # Using the provided transform function
        correct = np.array_equal(predicted_output, output_grid)
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'correct': correct
        })
    return results
example_task = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [3, 0, 0, 0, 0, 0, 0, 0, 0, 3], [3, 0, 0, 3, 0, 0, 3, 0, 0, 3], [3, 0, 0, 3, 0, 0, 3, 0, 0, 3], [3, 0, 0, 3, 0, 0, 3, 0, 0, 3], [3, 0, 0, 3, 0, 0, 3, 0, 0, 3], [3, 0, 0, 3, 0, 0, 3, 0, 0, 3], [3, 0, 0, 3, 0, 0, 3, 0, 0, 3], [3, 0, 0, 0, 0, 0, 0, 0, 0, 3], [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]},
        {'input': [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], 'output': [[3, 3, 3, 3, 3, 3, 3], [3, 0, 0, 0, 0, 0, 3], [3, 0, 0, 3, 0, 0, 3], [3, 0, 0, 3, 0, 0, 3], [3, 0, 0, 3, 0, 0, 3], [3, 0, 0, 0, 0, 0, 3], [3, 3, 3, 3, 3, 3, 3]]},
        {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], 'output': [[3, 3, 3, 3, 3, 3], [3, 0, 0, 0, 0, 3], [3, 0, 0, 3, 0, 3], [3, 0, 0, 3, 0, 3], [3, 0, 0, 0, 0, 3], [3, 3, 3, 3, 3, 3]]}
    ]
}

results = analyze_results(example_task)
for r in results:
    print(r)