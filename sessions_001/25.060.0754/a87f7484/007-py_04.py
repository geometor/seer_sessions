import numpy as np

def analyze_results(examples, transform_func):
    results = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        expected_output = example["output"]
        actual_output = transform_func(input_grid)
        
        # Basic grid comparison
        is_correct = np.array_equal(np.array(actual_output), np.array(expected_output))

        results.append({
            "example_index": i,
            "input_shape": np.array(input_grid).shape,
            "output_shape": np.array(expected_output).shape,
            "actual_output_shape": np.array(actual_output).shape,
            "is_correct": is_correct,
            "input_grid": input_grid,
            "expected_output": expected_output,
            "actual_output": actual_output
        })
    return results

# Assuming 'task' is a dictionary containing the 'train' examples
# You'll need to replace this with the actual task data structure
task = {
    "train": [
        {"input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], "output": [[8, 8, 8], [8, 8, 8], [8, 8, 8]]},
        {"input": [[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 8, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]], "output": [[5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5], [8, 8, 8, 8, 8, 5, 8, 8, 8, 8, 8], [5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 8, 5, 5, 5, 5, 5]]},
        {"input": [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 3, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]], "output": [[3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3]]},
    ]
}
results = analyze_results(task["train"], transform)

for result in results:
    print(f"Example {result['example_index'] + 1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Actual Output Shape: {result['actual_output_shape']}")
    print(f"  Correct: {result['is_correct']}")
    if not result['is_correct']:
        print(f"   Input: {result['input_grid']}")
        print(f"   Expected: {result['expected_output']}")
        print(f"   Actual: {result['actual_output']}")
    print("-" * 20)