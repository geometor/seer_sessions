import numpy as np

# Provided task data (replace with actual data loading if necessary)
train_tasks = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 7, 0],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 7, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    },
     {
        "input": np.array([[0, 0, 0, 7, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    }
]

def find_orange_pixel(grid):
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 7:
                return r, c
    return None

results = []
for i, task in enumerate(train_tasks):
    input_grid = task['input']
    output_grid = task['output']
    input_orange = find_orange_pixel(input_grid)
    output_oranges = []
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r,c] == 7:
                output_oranges.append((r,c))

    results.append({
        "task_index": i,
        "input_orange": input_orange,
        "output_oranges": output_oranges,
        "input_width": input_grid.shape[1],
        "output_width": output_grid.shape[1]
    })

print(results)