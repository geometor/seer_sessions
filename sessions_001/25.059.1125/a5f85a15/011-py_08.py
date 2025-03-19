# Assume this is the 'code_execution' part, providing example data.

def simulate_code_execution(transform, train_examples):
    results = []
    for example in train_examples:
        input_grid = example['input']
        expected_output_grid = example['output']
        actual_output_grid = transform(input_grid)
        results.append({
          'input': input_grid.tolist(), 'expected': expected_output_grid.tolist(),
          'actual': actual_output_grid.tolist(),
          'match': np.array_equal(expected_output_grid, actual_output_grid)
        })
        
    return results

#Hypothetical ARC Task Examples:

train_examples = [
    {
        'input': np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
        'output': np.array([[1, 1, 1], [1, 4, 1], [1, 1, 1]]),
    },
    {
        'input': np.array([[2, 2, 2, 2, 2], [2, 2, 2, 2, 2]]),
        'output': np.array([[2, 2, 2, 2, 2], [2, 2, 4, 2, 2]]),
    },
    {
        'input': np.array([[3, 3], [3, 3], [3, 3], [3, 3]]),
        'output': np.array([[3, 3], [3, 4], [3, 3], [3, 3]]),
    },
]
results = simulate_code_execution(transform, train_examples)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input:\n{np.array(result['input'])}")
    print(f"  Expected Output:\n{np.array(result['expected'])}")
    print(f"  Actual Output:\n{np.array(result['actual'])}")
    print(f"  Match: {result['match']}")
