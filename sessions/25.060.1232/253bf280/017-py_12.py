import numpy as np

def get_counts(grid,value):
    rows, cols = grid.shape
    count = 0
    for r in range(rows):
        indices = np.where(grid[r] == value)[0]
        count += len(indices)
    return count

def get_result(grid,r,value):
    indices = np.where(grid[r] == value)[0]
    return len(indices)

def analyze_training_data(task_data):
    analysis = {}
    for example_index, example in enumerate(task_data['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        input_8_count = get_counts(input_grid, 8)
        input_3_count = get_counts(input_grid, 3)
        output_8_count = get_counts(output_grid, 8)
        output_3_count = get_counts(output_grid, 3)
        
        predicted_grid = transform(input_grid)
        rows, cols = input_grid.shape
        result = "pass"
        if not np.array_equal(predicted_grid,output_grid):
          result = "fail"
        
        row_details = []
        for r in range(rows):
          row_details.append(f"Row {r}: 8s={get_result(input_grid,r,8)}, predicted 3s={get_result(predicted_grid,r,3)}, output 3s={get_result(output_grid,r,3)}")

        analysis[f'example_{example_index + 1}'] = {
            'input_grid_shape': input_grid.shape,
            'output_grid_shape': output_grid.shape,
            'input_8_count': input_8_count,
            'input_3_count': input_3_count,
            'output_8_count': output_8_count,
            'output_3_count': output_3_count,
            'predicted_vs_output': result,
            'row_details':row_details
        }
    return analysis

# Assuming 'task' is your dictionary loaded from JSON
import json
with open('6b6a9f85.json', 'r') as f:
    task = json.load(f)

analysis = analyze_training_data(task)

for key, value in analysis.items():
    print(f"{key}:")
    for k, v in value.items():
        print(f"  {k}: {v}")