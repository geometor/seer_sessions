import numpy as np

def get_grid_dimensions(grid_str):
    rows = grid_str.strip().split('\n')
    height = len(rows)
    width = len(rows[0].split())
    return height, width

def analyze_example(input_str, output_str, predicted_str):
    input_height, input_width = get_grid_dimensions(input_str)
    output_height, output_width = get_grid_dimensions(output_str)
    predicted_height, predicted_width = get_grid_dimensions(predicted_str)

    # determine where the cross is located
    output_grid = np.array([list(map(int, row.split())) for row in output_str.strip().split('\n')])
    
    # Find the row index of the horizontal line
    horizontal_line_row = -1
    for r in range(output_height):
        if np.all(output_grid[r, :] == 8):
            horizontal_line_row = r
            break

    # Find the column index of the vertical line
    vertical_line_col = -1
    for c in range(output_width):
        if np.all(output_grid[:, c] == 8):
            vertical_line_col = c
            break

    # determine correctness - are all non-zero predicted values correct
    predicted_grid = np.array([list(map(int, row.split())) for row in predicted_str.strip().split('\n')])
    correct = np.all(predicted_grid[predicted_grid != 0] == output_grid[predicted_grid != 0])

    print(f"  Input Dimensions: {input_height}x{input_width}")
    print(f"  Output Dimensions: {output_height}x{output_width}")
    print(f"  Predicted Dimensions: {predicted_height}x{predicted_width}")
    print(f"  Horizontal Line Row: {horizontal_line_row}")
    print(f"  Vertical Line Col: {vertical_line_col}")
    print(f"  Correct: {correct}")
    print("-" * 20)

# retrieve data from the environment
examples = task_data['train']
test_input = task_data['test'][0]['input']

for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    input_str = example['input']
    output_str = example['output']

    input_grid = np.array([list(map(int, row.split())) for row in input_str.strip().split('\n')])
    predicted_grid = transform(input_grid)  # use the function name from the previous turn
    predicted_str = '\n'.join(' '.join(map(str, row)) for row in predicted_grid)

    analyze_example(input_str, output_str, predicted_str)

print("Test Input:")
print(test_input)
test_height, test_width = get_grid_dimensions(test_input)
print(f"Test Input Dimensions: {test_height}x{test_width}")
