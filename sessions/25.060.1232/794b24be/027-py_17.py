def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)  # Using the provided transform function

        # Find non-zero cells in input
        input_non_zero = np.where(input_grid != 0)
        input_non_zero_coords = list(zip(input_non_zero[0], input_non_zero[1]))
        input_non_zero_values = [input_grid[coord] for coord in input_non_zero_coords]

        # Find non-zero cells in the actual output
        output_non_zero = np.where(output_grid != 0)
        output_non_zero_coords = list(zip(output_non_zero[0], output_non_zero[1]))
        output_non_zero_values = [output_grid[coord] for coord in output_non_zero_coords]

        # Find non-zero cells in predicted output.
        predicted_non_zero = np.where(predicted_output != 0)
        predicted_non_zero_coords = list(zip(predicted_non_zero[0],predicted_non_zero[1]))
        predicted_non_zero_values = [output_grid[coord] for coord in predicted_non_zero_coords]

        results.append({
            'input_non_zero_coords': input_non_zero_coords,
            'input_non_zero_values': input_non_zero_values,
            'output_non_zero_coords': output_non_zero_coords,
            'output_non_zero_values': output_non_zero_values,
            'predicted_non_zero_coords': predicted_non_zero_coords,
            'predicted_non_zero_values': predicted_non_zero_values,
            'success': np.array_equal(output_grid, predicted_output)
        })
    return results

# Assuming 'task' variable contains the loaded task data
# results = analyze_examples(task)
# for i, result in enumerate(results):
#     print(f"Example {i+1}:")
#     print(f"  Input Non-zero Coords: {result['input_non_zero_coords']}")
#     print(f"  Input Non-zero Values: {result['input_non_zero_values']}")
#     print(f"  Output Non-zero Coords: {result['output_non_zero_coords']}")
#     print(f"  Output Non-zero Values: {result['output_non_zero_values']}")
#     print(f"  Predicted output Non-zero coords: {result['predicted_non_zero_coords']}")
#     print(f"  Predicted Output Non-zero values: {result['predicted_non_zero_values']}")
#     print(f"  Success: {result['success']}")


# Example output for illustration (replace with actual data from execution)
example_results = [
     {
        'input_non_zero_coords': [(2, 2)],
        'input_non_zero_values': [1],
        'output_non_zero_coords': [(0, 0)],
        'output_non_zero_values': [2],
        'predicted_non_zero_coords': [(0, 0)],
        'predicted_non_zero_values': [2],
        'success': True
    },
    {
        'input_non_zero_coords': [(1, 3), (2, 5)],
        'input_non_zero_values': [4, 6],
        'output_non_zero_coords': [(0, 0)],
        'output_non_zero_values': [2],
        'predicted_non_zero_coords': [(0,0)],
        'predicted_non_zero_values': [2],
        'success': True
    },
    {
        'input_non_zero_coords': [(0, 0), (4,4)],
        'input_non_zero_values': [3,8],
        'output_non_zero_coords': [(0, 0)],
        'output_non_zero_values': [2],
        'predicted_non_zero_coords': [(0,0)],
        'predicted_non_zero_values': [2],
        'success': True

    }
]
