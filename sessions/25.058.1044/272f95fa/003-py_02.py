# Conceptual Code - for illustrative purposes only. Cannot be executed directly.

def analyze_results(task_data, transform_function):
    results = {}
    for example_id, example in enumerate(task_data['train']):
        input_grid = example['input']
        expected_output_grid = example['output']
        predicted_output_grid = transform_function(input_grid)
        is_correct = predicted_output_grid == expected_output_grid

        # Metrics
        azure_lines_input = find_azure_lines(np.array(input_grid))
        azure_lines_output = find_azure_lines(np.array(expected_output_grid)) # important to see if the function removes the correct lines

        results[f'example_{example_id}'] = {
            'correct': is_correct,
            'input_azure_lines': azure_lines_input,
            'output_azure_lines': azure_lines_output,
            'predicted_output': predicted_output_grid, #for visual inspection
            'expected_output': expected_output_grid

        }
    return results

# Hypothetical Results (Illustrative) - Assuming 'task_data' is loaded.
# results = analyze_results(task_data, transform)
# print(results)