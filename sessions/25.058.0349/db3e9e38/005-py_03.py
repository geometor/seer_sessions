def get_metrics(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid.copy())
        comparison = predicted_output == output_grid
        all_match = np.all(comparison)
        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'all_match': all_match,
            'comparison_grid': comparison.tolist(),
            'predicted_output': predicted_output.tolist(),
        })
    return results

# Assuming 'task' is defined elsewhere and contains the input/output examples
# Replace 'task' with the actual variable name containing the task data

task = {
 'train': [
    {'input': [[7, 0, 7], [0, 7, 0], [7, 0, 7]], 'output': [[8, 8, 8], [8, 7, 8], [8, 8, 8]]},
    {'input': [[0, 7, 0, 7], [0, 0, 0, 0], [7, 0, 7, 0], [0, 0, 0, 0]], 'output': [[8, 7, 8, 7], [8, 8, 8, 8], [7, 8, 7, 8], [8, 8, 8, 8]]},
    {'input': [[7, 0, 0, 0, 0], [0, 0, 0, 0, 7]], 'output': [[7, 8, 8, 8, 8], [8, 8, 8, 8, 7]]}
 ]
}
results = get_metrics(task)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  All Match: {result['all_match']}")
    if not result['all_match']:
        print("  Mismatches:")
        mismatches = np.array(result['comparison_grid']) == False
        input_grid = np.array(task['train'][i]['input'])
        output_grid = np.array(task['train'][i]['output'])
        predicted_output = np.array(result['predicted_output'])

        mismatch_indices = np.where(mismatches)
        for row, col in zip(*mismatch_indices):
            print(f"    Location (row, col): ({row}, {col})")
            print(f"      Input Value : {input_grid[row, col]}")
            print(f"      Expected Value: {output_grid[row, col]}")
            print(f"      Predicted Value: {predicted_output[row, col]}")
