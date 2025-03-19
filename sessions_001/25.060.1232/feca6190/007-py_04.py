import numpy as np

def get_grid_dimensions(grid):
    return len(grid), len(grid[0])

def count_non_zero_pixels(grid):
    return np.count_nonzero(grid)

def get_color_counts(grid):
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))
    

task_data = {
    "train": [
        {
            "input": [[5, 1, 8, 0, 2]],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 8, 2, 0, 0, 0, 0],
                [0, 0, 0, 1, 8, 8, 2, 0, 0, 0],
                [0, 0, 5, 1, 1, 8, 8, 2, 0, 0],
                [0, 5, 5, 1, 1, 1, 8, 8, 2, 0],
            ],
        },
        {
            "input": [[0, 1, 2, 3, 4]],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 4, 0, 0, 0, 0, 0],
                [0, 0, 2, 3, 3, 4, 0, 0, 0, 0],
                [0, 1, 2, 2, 3, 3, 4, 0, 0, 0],
                [1, 1, 2, 2, 2, 3, 3, 4, 0, 0],
                [1, 1, 1, 2, 2, 2, 3, 3, 4, 0],
            ],
        },
        {
            "input": [[9, 9, 9, 9, 9]],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
                [0, 0, 0, 9, 9, 0, 0, 0, 0, 0],
                [0, 0, 9, 9, 9, 0, 0, 0, 0, 0],
                [0, 9, 9, 9, 9, 0, 0, 0, 0, 0],
                [9, 9, 9, 9, 9, 0, 0, 0, 0, 0],
                [9, 9, 9, 9, 9, 0, 0, 0, 0, 0]
            ],
        },
    ],
    "test": [
        {"input": [[7, 5, 9, 1, 3]]},
    ],
}

def analyze_results(task_data):
  analysis = {}
  for task_type in task_data:
    analysis[task_type] = []    
    for i, example in enumerate(task_data[task_type]):
        input_grid = example['input']
        expected_output_grid = example['output']

        # Call the transform function
        transformed_grid = transform(input_grid)
        
        result = {
            "input_dimensions": get_grid_dimensions(input_grid),
            "output_dimensions": get_grid_dimensions(expected_output_grid),
            "transformed_dimensions": get_grid_dimensions(transformed_grid),
            "input_non_zero_pixels": count_non_zero_pixels(input_grid),
            "output_non_zero_pixels": count_non_zero_pixels(expected_output_grid),
            "transformed_non_zero_pixels": count_non_zero_pixels(transformed_grid),
            "input_color_counts": get_color_counts(input_grid),
            "output_color_counts": get_color_counts(expected_output_grid),
            "transformed_color_counts": get_color_counts(transformed_grid),
            "grids_match": np.array_equal(transformed_grid, expected_output_grid)
        }
        analysis[task_type].append(result)
  return analysis

results = analyze_results(task_data)

# use a loop to print the results so it all fits within the max message length
for task_type in results:
  print(f"Task Type: {task_type}")
  for i, result in enumerate(results[task_type]):
    print(f'Example: {i + 1}')
    print(result)
