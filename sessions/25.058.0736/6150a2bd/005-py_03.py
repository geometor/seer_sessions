import numpy as np

def analyze_results(task_data):
    results = []
    for example in task_data['train']:
        input_grid = example['input']
        expected_output = example['output']
        
        # Convert to numpy arrays for easier processing
        input_np = np.array(input_grid)
        expected_output_np = np.array(expected_output)

        # Apply the transformation
        predicted_output_np = np.rot90(input_np, k=-1)
        
        # Basic metrics
        correct = np.array_equal(predicted_output_np, expected_output_np)
        input_shape = input_np.shape
        output_shape = expected_output_np.shape
        predicted_shape = predicted_output_np.shape

        results.append({
            'correct': correct,
            'input_shape': input_shape,
            'output_shape': output_shape,
            'predicted_shape': predicted_shape
        })

    return results

# dummy task data - replace with your provided data
task_data = {
    'train': [
        {'input': [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 'output': [[7, 4, 1], [8, 5, 2], [9, 6, 3]]},
        {'input': [[0, 1], [2, 3]], 'output': [[2, 0], [3, 1]]},
        {'input': [[5]], 'output': [[5]]}
    ]
}

analysis = analyze_results(task_data)

for i, result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Correct: {result['correct']}")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Predicted Shape: {result['predicted_shape']}")
    print("-" * 20)
