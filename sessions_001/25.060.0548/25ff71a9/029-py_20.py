import numpy as np

def get_grid_differences(grid1, grid2):
    """
    Compares two grids and returns a list of differences.
    Each difference is a tuple: (row, col, old_value, new_value)
    """
    differences = []
    for r in range(grid1.shape[0]):
        for c in range(grid1.shape[1]):
            if grid1[r, c] != grid2[r, c]:
                differences.append((r, c, grid1[r, c], grid2[r, c]))
    return differences

def analyze_task(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid) #uses previous transform function
        differences = get_grid_differences(output_grid, predicted_output)
        print(f"  Example {i+1}:")
        print(f"    Input shape: {input_grid.shape}")
        print(f"    Output shape: {output_grid.shape}")
        print(f"    Differences between Expected and Predicted Output: {differences}")

# Example usage with a hypothetical task structure (replace with actual task data)

TASKS = [
   {'name': 'Task 1',
    'train': [
        {'input': [[5, 5, 5], [5, 2, 5], [5, 5, 5]], 'output': [[5, 5, 5], [5, 5, 5], [5, 2, 5]]},
        {'input': [[0, 0, 0, 2, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 2, 0]]},
        {'input': [[0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0]]}
    ],
    'test': [{'input': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 2, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 2, 0]]}]
   },
]

for task in TASKS:
  analyze_task(task)
