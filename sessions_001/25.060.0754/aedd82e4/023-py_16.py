import numpy as np

def analyze_results(task_name, examples):
    results = []
    for example_num, example in enumerate(examples):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        actual_output = transform(input_grid)

        rows, cols = input_grid.shape
        center_row, center_col = rows // 2, cols // 2

        # Center Pixel Analysis
        center_input = input_grid[center_row, center_col]
        center_expected = expected_output[center_row, center_col]
        center_actual = actual_output[center_row, center_col]

        # Red Pixel Analysis
        red_pixels_input = np.argwhere(input_grid == 2)
        red_pixels_expected = np.argwhere(expected_output == 2)
        red_pixels_actual = np.argwhere(actual_output == 2)

        red_preserved = all((pos in red_pixels_actual) for pos in red_pixels_input if not (pos[0]==center_row and pos[1]==center_col))
        

        # White Pixel Analysis around center
        white_to_blue_expected = []
        
        # look at the expected output
        for i in range(rows):
            for j in range(cols):
                if input_grid[i,j] == 0:
                    if expected_output[i,j] == 1:
                         white_to_blue_expected.append((i,j))
        
        white_to_blue_actual = []
        for i in range(rows):
            for j in range(cols):
                if input_grid[i, j] == 0:
                    if actual_output[i,j] == 1:
                         white_to_blue_actual.append((i,j))


        results.append({
            'example': example_num + 1,
            'center_input': int(center_input),
            'center_expected': int(center_expected),
            'center_actual': int(center_actual),
            'red_preserved': bool(red_preserved),
            'white_to_blue_expected' : white_to_blue_expected,
            'white_to_blue_actual' : white_to_blue_actual
        })

    return results

# Assuming 'train' contains the training examples
# You would need to replace 'train' with the actual variable holding your examples

#example usage - requires the 'train' variable in the context
task_name = "Example Task"  # Replace with the actual task name
# analyzed_results = analyze_results(task_name, train)
# print(analyzed_results)