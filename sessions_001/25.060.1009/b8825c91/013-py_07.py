import numpy as np

def analyze_examples(examples):
    results = []
    for example in examples:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)
        
        # Basic Grid Properties
        input_shape = input_grid.shape
        output_shape = output_grid.shape
        predicted_shape = predicted_output.shape
        shapes_match = output_shape == predicted_shape
        
        # Pixel-wise comparison
        correct_pixels = np.sum(output_grid == predicted_output)
        total_pixels = output_grid.size
        accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0

        results.append({
            'input_shape': input_shape,
            'output_shape': output_shape,
            'predicted_shape': predicted_shape,
            'shapes_match': shapes_match,
            'correct_pixels': correct_pixels,
            'total_pixels': total_pixels,
            'accuracy': accuracy
        })
    return results
examples = [
    {'input': [[4, 4, 4, 4, 4, 4, 4, 4]], 'output': [[1, 1, 1, 1, 1, 1, 1, 1]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [4, 4, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 4, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[4, 4, 0, 4, 4, 4, 0, 4], [0, 0, 0, 4, 4, 4, 0, 0]], 'output': [[1, 1, 0, 1, 1, 1, 0, 4], [0, 0, 0, 4, 4, 4, 0, 0]]}
]

analysis_results = analyze_examples(examples)

for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Predicted Shape: {result['predicted_shape']}")
    print(f"  Shapes Match: {result['shapes_match']}")
    print(f"  Correct Pixels: {result['correct_pixels']}")
    print(f"  Total Pixels: {result['total_pixels']}")
    print(f"  Accuracy: {result['accuracy']:.2f}")
    print("-" * 20)