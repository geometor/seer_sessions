import numpy as np

def analyze_results(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        predicted_output = transform(input_grid)  # Using the provided transform function
        correct = np.array_equal(predicted_output, expected_output)
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': predicted_output.shape,
            'expected_shape': expected_output.shape,
            'correct': correct,
            'predicted_output': predicted_output.tolist(),  # For easy viewing
            'expected_output': expected_output.tolist()
        })
    return results

# Assuming 'task' variable holds the task data (from JSON)
# you may need to adapt this line
task_data = task # replace with actual data load
analysis = analyze_results(task_data)

for i, result in enumerate(analysis):
    print(f"--- Example {i+1} ---")
    print(f"Input Shape: {result['input_shape']}")
    print(f"Predicted Output Shape: {result['output_shape']}")
    print(f"Expected Output Shape: {result['expected_shape']}")
    print(f"Correct: {result['correct']}")
    print(f"Predicted Output:\n{np.array(result['predicted_output'])}")
    print(f"Expected Output:\n{np.array(result['expected_output'])}")
    print()
