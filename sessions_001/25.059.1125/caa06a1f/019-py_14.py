import numpy as np

#Dummy examples based on transformation.
train_examples = [
    {
        'input': np.array([[1, 1, 1], [8, 8, 8], [1, 1, 1]]),
        'output': np.array([[1, 1, 1], [8, 8, 8]])
    },
    {
        'input': np.array([[8, 8, 1], [8, 8, 1], [1, 1, 1]]),
        'output': np.array([[8, 8, 8], [8, 8, 1], [1, 1, 1]])
    },
     {
        'input': np.array([[1, 1, 1, 1], [8, 8, 8, 8], [8, 8, 8, 8], [1, 1, 1, 1]]),
        'output': np.array([[1, 1, 1, 1], [8, 8, 8, 8], [8, 8, 8, 8]])
    },
    {
        'input': np.array([[1, 1, 1, 8], [1, 1, 1, 8], [8, 8, 8, 1]]),
        'output': np.array([[1, 1, 1, 1], [1, 1, 1, 8], [8, 8, 8, 1]])
    },
    {
        'input': np.array([[8, 8, 8, 8, 8], [8, 8, 8, 8, 8], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]),
        'output': np.array([[8, 8, 8, 8, 8], [8, 8, 8, 8, 8], [1, 1, 1, 1, 1]])
    }
]

def analyze_examples(examples, transform_func):
    results = []
    for i, example in enumerate(examples):
        input_grid = example['input']
        expected_output = example['output']
        predicted_output = transform_func(input_grid.copy())  # Use a copy to avoid modifying the original

        # Basic structural comparison.
        correct_shape = predicted_output.shape == expected_output.shape
        correct_values = np.array_equal(predicted_output, expected_output)
        all_correct = correct_shape and correct_values

        results.append({
            'example_index': i,
            'input_shape': input_grid.shape,
            'output_shape': expected_output.shape,
            'predicted_shape': predicted_output.shape,
            'correct_shape': correct_shape,
            'correct_values': correct_values,
            'all_correct': all_correct,

        })
    return results

from previous_response import transform #Import transform from above.
analysis_results = analyze_examples(train_examples, transform)

for result in analysis_results:
    print(result)