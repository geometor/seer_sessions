import numpy as np

def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)
        correct = np.array_equal(predicted_output, output_grid)
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'predicted_output_shape': predicted_output.shape,
            'correct': correct,
            'input_colors': np.unique(input_grid).tolist(),
            'output_colors': np.unique(output_grid).tolist(),
            'predicted_output_colors': np.unique(predicted_output).tolist(),
        })
    return results

# Example Usage with the provided task data (replace with actual task data)
task = {
    "train": [
        {
            "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
            "output": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
        },
        {
            "input": [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]],
            "output": [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]],
        },
        {
            "input": [[0, 5, 5, 5, 0], [0, 5, 5, 5, 0], [0, 5, 5, 5, 0], [0, 5, 5, 5, 0], [0, 5, 5, 5, 0]],
            "output": [[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5], [5, 0, 0, 0, 0, 0, 0, 5], [5, 0, 0, 0, 0, 0, 0, 5], [5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5, 5], [5, 0, 0, 0, 0, 0, 0, 5], [5, 0, 0, 0, 0, 0, 0, 5], [5, 5, 5, 5, 5, 5, 5, 5]],
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 0, 0, 5, 5, 5], [5, 5, 5, 0, 0, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5]],
        },
    ]
}
results = analyze_results(task)
for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Correct: {res['correct']}")
    print(f"  Input Colors: {res['input_colors']}")
    print(f"  Output Colors: {res['output_colors']}")
    print(f"  Predicted Output Colors: {res['predicted_output_colors']}")