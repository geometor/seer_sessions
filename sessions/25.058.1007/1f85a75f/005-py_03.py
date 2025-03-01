import numpy as np

def find_green_square(grid):
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == 3 and grid[i + 1, j] == 3 and
                grid[i, j + 1] == 3 and grid[i + 1, j + 1] == 3):
                return (i, j)
    return None

def analyze_examples(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        green_square_coords = find_green_square(input_grid)

        print(f"  Example {i + 1}:")
        print(f"    Input shape: {input_grid.shape}")
        print(f"    Output shape: {output_grid.shape}")

        if green_square_coords:
            print(f"    Green square found at: {green_square_coords}")
        else:
            print(f"    Green square not found.")

# Placeholder for the task data - replace with actual data
task_data = {
    'name': 'Example Task',
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 3, 3, 0, 0],
                   [0, 0, 0, 3, 3, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0]],
         'output': [[3, 3, 3],
                    [3, 3, 3],
                    [0, 0, 3]]},
        {'input': [[0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 3, 3, 0],
                   [0, 0, 0, 3, 3, 0],
                   [0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0]],
         'output': [[3, 3, 3],
                    [3, 3, 3]]},
        {'input': [[0, 0, 0, 0, 0],
                   [0, 0, 3, 3, 0],
                   [0, 0, 3, 3, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]],
         'output': [[3, 3, 3],
                    [3, 3, 3]]},
    ]
}

analyze_examples(task_data)
