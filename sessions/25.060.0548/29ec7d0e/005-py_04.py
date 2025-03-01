example_results = []
#dummy data - need actual examples to be valuable
input_grid = [[1, 0, 1], [1, 1, 1], [0, 0, 0]]
output_grid = [[1, 2, 1], [1, 1, 1], [2, 2, 2]]
predicted_grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
example_results.append(analyze_example(input_grid, output_grid,
predicted_grid))

input_grid = [[0, 2, 0], [2, 2, 2], [0, 2, 0]]
output_grid = [[1, 2, 1], [1, 2, 1], [1, 2, 1]]
predicted_grid = [[1, 2, 1], [1, 2, 1], [1, 2, 1]]
example_results.append(analyze_example(input_grid, output_grid, predicted_grid))

for i, metrics in enumerate(example_results):
    print(f"Example {i+1}:")
    print(f"  Correct: {metrics['correct']}")
    print(f"  Input Zero Count: {metrics['input_zero_count']}")
    print(f"  Output Zero Count: {metrics['output_zero_count']}")
    print(f"  Same shape: {metrics['same_shape']}")
    print(f"Difference:\n {metrics['difference']}")