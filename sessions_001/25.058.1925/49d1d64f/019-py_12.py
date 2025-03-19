import numpy as np

def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)
        
        input_rows, input_cols = input_grid.shape
        output_rows, output_cols = output_grid.shape
        predicted_rows, predicted_cols = predicted_output.shape
        
        correct = np.array_equal(output_grid, predicted_output)

        results.append({
            'input_shape': (input_rows, input_cols),
            'output_shape': (output_rows, output_cols),
            'predicted_shape': (predicted_rows, predicted_cols),
            'correct': correct,
            'output_grid': output_grid.tolist(),
            'predicted_output': predicted_output.tolist()
        })
    return results

task = {
    'train': [
        {'input': [[1, 2], [3, 4]], 'output': [[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]]},
        {'input': [[5, 6, 7]], 'output': [[0, 0, 0, 0, 0], [0, 5, 6, 7, 0], [0, 0, 0, 0, 0]]},
        {'input': [[8], [9]], 'output': [[0, 0, 0], [0, 8, 0], [0, 9, 0], [0, 0, 0]]}
    ]
}

analysis = analyze_results(task)

for i, result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Predicted Shape: {result['predicted_shape']}")
    print(f"  Correct: {result['correct']}")
    print(f"  Output grid: {result['output_grid']}")    
    print(f"  Predicted Output: {result['predicted_output']}")
    print("-" * 20)