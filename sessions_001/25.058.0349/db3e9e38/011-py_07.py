import numpy as np

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)  # Using the provided transform function
        is_correct = np.array_equal(predicted_output_grid, expected_output_grid)

        # Find orange pixels in input
        orange_pixels_input = np.where(input_grid == 7)
        orange_pixels_input_coords = list(zip(orange_pixels_input[0], orange_pixels_input[1]))
        
        #find orange pixels in output
        orange_pixels_output = np.where(expected_output_grid == 7)
        orange_pixels_output_coords = list(zip(orange_pixels_output[0], orange_pixels_output[1]))

        #find azure pixels in output
        azure_pixels_output = np.where(expected_output_grid == 8)
        azure_pixels_output_coords = list(zip(azure_pixels_output[0], azure_pixels_output[1]))

        results.append({
            'example_index': i,
            'input_shape': input_grid.shape,
            'output_shape': expected_output_grid.shape,
            'prediction_correct': is_correct,
            'orange_pixels_input': orange_pixels_input_coords,
            'orange_pixels_output': orange_pixels_output_coords,
            'azure_pixels_output': azure_pixels_output_coords
        })
    return results

# Assuming 'task' variable holds the task data as described in the problem
examples = task["train"]

analysis_results = analyze_examples(examples)

for result in analysis_results:
    print(result)
