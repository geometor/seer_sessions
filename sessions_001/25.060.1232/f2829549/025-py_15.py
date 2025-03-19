import numpy as np

def analyze_example(input_grid, expected_output_grid, predicted_output_grid):
    blue_line_column = -1
    for j in range(input_grid.shape[1]):
        if np.all(input_grid[:, j] == 1):
            blue_line_column = j
            break

    input_dims = input_grid.shape
    expected_output_dims = expected_output_grid.shape
    predicted_output_dims = predicted_output_grid.shape if predicted_output_grid is not None else (0,0)

    input_colors = np.unique(input_grid)
    expected_output_colors = np.unique(expected_output_grid)
    predicted_output_colors = np.unique(predicted_output_grid) if predicted_output_grid is not None else []

    correct = np.array_equal(expected_output_grid,predicted_output_grid)

    print(f"  Blue Line Column: {blue_line_column}")
    print(f"  Input Dimensions: {input_dims}")
    print(f"  Expected Output Dimensions: {expected_output_dims}")
    print(f"  Predicted Output Dimensions: {predicted_output_dims}")
    print(f"  Input Colors: {input_colors}")
    print(f"  Expected Output Colors: {expected_output_colors}")
    print(f"  Predicted Output Colors: {predicted_output_colors}")
    print(f"  Correct prediction?: {correct}")

#from previous interactions
task_id = '08ed6ac7'
examples = task_data[task_id]['train']

for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    input_grid = np.array(example['input'])
    expected_output_grid = np.array(example['output'])
    # transform function must be in scope when this is executed
    predicted_output_grid = transform(input_grid)
    analyze_example(input_grid, expected_output_grid, predicted_output_grid)
