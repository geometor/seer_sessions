def grid_diff(grid1, grid2):
    """Counts the number of differing pixels between two grids."""
    return np.sum(grid1 != grid2)

def analyze_results(task):
    """Analyzes the results of applying the transform function to task examples."""
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        transformed_grid = transform(input_grid)  # use existing transform function
        diff_count = grid_diff(transformed_grid, expected_output)
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': expected_output.shape,
            'diff_count': diff_count,
             'transformed_grid': transformed_grid.tolist(),  # For easier viewing
            'expected_output': expected_output.tolist() #also for easier viewing
        })
    return results

task = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 1, 8, 8, 1, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 1, 6, 6, 1, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 8, 1, 0, 0, 0], [0, 0, 1, 8, 8, 8, 1, 0, 0], [0, 0, 0, 1, 8, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 6, 1, 0, 0, 0], [0, 0, 1, 6, 6, 6, 1, 0, 0], [0, 0, 0, 1, 6, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 1, 3, 3, 3, 1, 0, 0, 0], [0, 0, 1, 3, 3, 3, 1, 0, 0, 0], [0, 0, 1, 3, 3, 3, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 1, 6, 6, 6, 1, 0, 0, 0], [0, 0, 1, 6, 6, 6, 1, 0, 0, 0], [0, 0, 1, 6, 6, 6, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]}
    ]
}

results = analyze_results(task)
for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {res['input_shape']}")
    print(f"  Output Shape: {res['output_shape']}")
    print(f"  Differences: {res['diff_count']}")
    #print(f"  Transformed Grid:\n{np.array(res['transformed_grid'])}")
    #print(f"  Expected Output:\n{np.array(res['expected_output'])}")