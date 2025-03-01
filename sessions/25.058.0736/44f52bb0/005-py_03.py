import numpy as np

def get_metrics(grid):
    metrics = {
        'red_count': np.sum(grid == 2),
        'blue_count': np.sum(grid == 1),
        'white_count': np.sum(grid == 0),
        'height': grid.shape[0],
        'width': grid.shape[1]
    }
    return metrics
input_grids = [
    np.array([[6, 1, 1],
              [1, 1, 1],
              [5, 1, 2]]),
    np.array([[0, 3, 0, 5, 3, 0, 3, 0, 0],
             [5, 0, 5, 0, 0, 0, 5, 5, 5],
             [0, 0, 3, 3, 3, 0, 0, 3, 0],
             [0, 3, 0, 0, 5, 0, 0, 3, 3],
             [0, 0, 5, 0, 3, 0, 0, 0, 0],
             [5, 3, 0, 0, 3, 0, 3, 5, 5],
             [8, 0, 0, 0, 0, 5, 8, 8, 5],
             [0, 0, 5, 8, 0, 8, 0, 5, 5],
             [8, 8, 0, 5, 0, 5, 8, 8, 8]]),
     np.array([[7, 0, 7, 7, 7, 0, 7, 0, 0],
             [7, 0, 0, 0, 7, 7, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 7, 7, 0, 0, 0, 0, 0, 7],
             [0, 0, 0, 7, 0, 0, 0, 7, 0],
             [0, 7, 0, 0, 7, 0, 7, 0, 7],
             [0, 0, 0, 7, 0, 0, 7, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]])
]
output_grids = [
    np.array([[1]]),
    np.array([[0]]),
    np.array([[0]])
]

for i, (input_grid, output_grid) in enumerate(zip(input_grids, output_grids)):
    input_metrics = get_metrics(input_grid)
    output_metrics = get_metrics(output_grid)
    print(f"Example {i+1}:")
    print(f"  Input: red_count={input_metrics['red_count']},  output_pixel={output_grid[0,0]}")

