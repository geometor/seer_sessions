import numpy as np

def find_boundary(grid):
    for col in range(grid.shape[1] - 1):
        if grid[0, col] != grid[0, col+1]:
            return col + 1
    return grid.shape[1] // 2

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        boundary_col = find_boundary(input_grid)

        #get background color
        background_color_left = input_grid[0,0]
        background_color_right = input_grid[0,boundary_col]

        results.append({
            'example_index': i,
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'boundary_column': boundary_col,
            'background_color_left': background_color_left,
            'background_color_right': background_color_right
        })
    return results

# Assuming 'task' is defined elsewhere and contains the training examples
example_data = analyze_examples(task['train'])
for item in example_data:
    print(item)