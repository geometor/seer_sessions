import numpy as np

def analyze_results(task_data):
    """Analyzes the results of applying the transform function to the task data.

    Args:
        task_data: A dictionary containing the task examples, including inputs,
          expected outputs, and transform outputs.

    Returns:
        A dictionary containing analysis results for each example.
    """
    results = {}
    for example_name, example_data in task_data.items():
        input_grid = np.array(example_data['input'])
        expected_output = np.array(example_data['output'])
        transform_output = np.array(example_data['transform'])

        # Compare transform output with expected output
        is_correct = np.array_equal(transform_output, expected_output)

        # Find blue and gray pixels in input
        blue_pixels_input = np.where(input_grid == 1)
        gray_pixels_input = np.where(input_grid == 5)

        # Find blue and gray pixels in output
        blue_pixels_output = np.where(expected_output == 1)
        gray_pixels_output = np.where(expected_output == 5)
      

        results[example_name] = {
            'correct': is_correct,
            'input_blue_pixels': list(zip(blue_pixels_input[0].tolist(), blue_pixels_input[1].tolist())),
            'input_gray_pixels': list(zip(gray_pixels_input[0].tolist(), gray_pixels_input[1].tolist())),
            'output_blue_pixels': list(zip(blue_pixels_output[0].tolist(), blue_pixels_output[1].tolist())),
            'output_gray_pixels': list(zip(gray_pixels_output[0].tolist(), gray_pixels_output[1].tolist())),
            'input_grid_shape': input_grid.shape,
            'output_grid_shape':expected_output.shape,
            'transform_equals_input': np.array_equal(transform_output,input_grid)
        }
    return results

# Create the task_data dictionary as it was structured in the test
# I will have to manually enter the data from the prompt
task_data = {
'example_1': {
            'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 5, 5, 5, 5, 5, 0, 0, 0]],
            'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                       [0, 0, 5, 5, 1, 5, 5, 0, 0, 0]],
            'transform': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                          [0, 0, 5, 5, 1, 5, 5, 0, 0, 0]]
        },
        'example_2': {
            'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 5, 5, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            'transform': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 5, 5, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        'example_3': {
            'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
                      [0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
                       [0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            'transform': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
                       [0, 0, 5, 5, 5, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        }
}

results = analyze_results(task_data)
print(results)