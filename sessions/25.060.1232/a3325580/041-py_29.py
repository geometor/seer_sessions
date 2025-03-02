import numpy as np

# Provided test cases (replace with actual data)
train_examples = [
  {
        "input": np.array([[1, 1, 1], [1, 5, 1], [1, 1, 1]]),
        "output": np.array([[1, 5]])
  },
   {
        "input": np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]),
        "output": np.array([[1]])
    },
    {
        "input": np.array([[2, 0, 0], [0, 3, 0], [0, 0, 4]]),
        "output": np.array([[2, 3, 4]])
    },
    {
        "input": np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
        "output": np.array([[5]])
    }
]
test_examples = []

def get_unique_colors(grid):
    return np.unique(grid[grid != 0])

def transform(input_grid):
    unique_colors = get_unique_colors(input_grid)
    num_colors = len(unique_colors)
    output_grid = np.zeros((1, num_colors), dtype=int)
    for index, val in enumerate(unique_colors):
        output_grid[0, index] = val
    return output_grid

def check_transform(examples):
    results = []
    for example in examples:
        input_grid = example["input"]
        expected_output = example["output"]
        actual_output = transform(input_grid)
        #compare using shape, and contents
        is_correct = np.array_equal(actual_output, expected_output)
        results.append({
            "input_shape": input_grid.shape,
            "output_shape": expected_output.shape,
            "actual_shape": actual_output.shape,
            "unique_input_colors": get_unique_colors(input_grid).tolist(),
            "unique_output_colors": get_unique_colors(expected_output).tolist(),
            "unique_actual_colors": get_unique_colors(actual_output).tolist(),
            "is_correct": is_correct
        })
    return results

train_results = check_transform(train_examples)
#test_results = check_transform(test_examples) # No test example given

for i, result in enumerate(train_results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Actual Shape: {result['actual_shape']}")
    print(f"  Unique Input Colors: {result['unique_input_colors']}")
    print(f"  Unique Output Colors: {result['unique_output_colors']}")
    print(f"  Unique Actual Colors: {result['unique_actual_colors']}")
    print(f"  Correct: {result['is_correct']}")