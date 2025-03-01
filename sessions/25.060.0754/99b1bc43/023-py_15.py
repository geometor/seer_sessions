import numpy as np

def check_examples(transform, examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        transformed_grid = transform(input_grid)
        is_correct = np.array_equal(transformed_grid, expected_output)

        results.append({
            'example_index': i,
            'input_shape': input_grid.shape,
            'output_shape': expected_output.shape,
            'is_correct': is_correct,
            'transformed_grid': transformed_grid.tolist(),  # Convert to list for easy viewing
            'expected_output': expected_output.tolist()
        })
    return results
examples = [
    {'input': [[0, 0, 2, 2, 5, 5], [0, 0, 2, 2, 5, 5], [2, 2, 0, 0, 6, 6], [2, 2, 0, 0, 6, 6], [4, 4, 4, 4, 7, 7], [4, 4, 4, 4, 7, 7]],
     'output': [[0, 0, 3, 3], [0, 0, 3, 3], [3, 3, 0, 0], [3, 3, 0, 0]]},
    {'input': [[0, 0, 1, 1, 9, 8], [0, 0, 1, 1, 9, 9], [1, 1, 0, 0, 7, 7], [1, 1, 0, 0, 5, 5], [4, 4, 4, 4, 5, 5], [4, 4, 4, 4, 5, 5]],
     'output': [[0, 0, 3, 3], [0, 0, 3, 3], [3, 3, 0, 0], [3, 3, 0, 0]]},
    {'input': [[5, 5, 0, 0, 1, 1], [6, 6, 0, 0, 1, 1], [7, 7, 1, 1, 0, 0], [7, 7, 1, 1, 0, 0], [8, 8, 4, 4, 4, 4], [9, 9, 4, 4, 4, 4]],
     'output': [[5, 5, 0, 0], [6, 6, 0, 0], [7, 7, 3, 3], [7, 7, 3, 3]]}
]
from previous_response import transform
results = check_examples(transform, examples)

for result in results:
   print(f"Example {result['example_index'] + 1}:")
   print(f"  Input shape: {result['input_shape']}")
   print(f"  Output shape: {result['output_shape']}")
   print(f"  Correct: {result['is_correct']}")
   print(f"  Transformed: {result['transformed_grid']}")
   print(f"  Expected: {result['expected_output']}")
   print("-" * 20)