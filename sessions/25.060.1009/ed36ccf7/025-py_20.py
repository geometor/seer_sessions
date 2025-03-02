import numpy as np

def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = example['input']
        expected_output = example['output']
        transformed_grid = transform(input_grid)  # Use the existing transform function

        input_shape = np.array(input_grid).shape
        expected_shape = np.array(expected_output).shape
        transformed_shape = np.array(transformed_grid).shape

        shape_match = (expected_shape == transformed_shape)
        
        if shape_match:
            correct_pixels = np.sum(np.array(transformed_grid) == np.array(expected_output))
            total_pixels = np.array(expected_output).size
            pixel_accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0
        else:
            pixel_accuracy = 0.0
            
        results.append({
            'input_shape': input_shape,
            'expected_shape': expected_shape,
            'transformed_shape': transformed_shape,
            'shape_match': shape_match,
            'pixel_accuracy': pixel_accuracy
        })
    return results

# Provided task data (replace with your actual task data structure)
task = {
    'train': [
        {'input': [[1, 2, 3]], 'output': [[1], [2], [3]]},
        {'input': [[5, 6], [7, 8]], 'output': [[5, 7], [6, 8]]},
        {'input': [[4, 4, 8], [4, 4, 8], [9, 9, 8]], 'output': [[4, 4, 8], [4, 4, 8], [9, 9, 8]]},
        {'input': [[5], [7], [7], [5], [5]], 'output': [[5, 7, 7, 5, 5]]},
        {'input': [[1, 2, 3, 4, 5, 6, 7, 8, 9]], 'output': [[1, 2, 3, 4, 5, 6, 7, 8, 9]]}
    ]
}

results = analyze_results(task)

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {res['input_shape']}")
    print(f"  Expected Shape: {res['expected_shape']}")
    print(f"  Transformed Shape: {res['transformed_shape']}")
    print(f"  Shape Match: {res['shape_match']}")
    print(f"  Pixel Accuracy: {res['pixel_accuracy']}")