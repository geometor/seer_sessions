def get_grid_metrics(grid):
    """Calculates basic metrics for a given grid."""
    n_rows = len(grid)
    n_cols = len(grid[0]) if n_rows > 0 else 0  # Handle empty grids
    unique_colors = set()
    for row in grid:
        for cell in row:
            unique_colors.add(cell)
    return {
        'rows': n_rows,
        'cols': n_cols,
        'unique_colors': list(unique_colors),
    }

def get_metrics_for_task(task):
    """Collects metrics for all input/output pairs in a task."""
    metrics = {}
    for i, pair in enumerate(task['train']):
        input_metrics = get_grid_metrics(pair['input'])
        output_metrics = get_grid_metrics(pair['output'])
        metrics[f'example_{i+1}'] = {
            'input': input_metrics,
            'output': output_metrics,
        }
    return metrics
task = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
            ]
        },
        {
            "input":[
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 7, 7, 7, 0, 0, 0],
                [0, 0, 0, 0, 7, 7, 7, 0, 0, 0],
                [0, 0, 0, 0, 7, 7, 7, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "output":[
                [7, 7, 7],
                [7, 7, 7],
                [7, 7, 7],
            ]
        },
                {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 4, 4, 0, 0, 0],
                [0, 0, 0, 0, 4, 4, 4, 0, 0, 0],
                [0, 0, 0, 0, 4, 4, 4, 0, 0, 0],
            ],
            "output": [
                [4, 4, 4],
                [4, 4, 4],
                [4, 4, 4],
            ]
        },
        {
            "input": [
                [2, 2, 2],
                [2, 2, 2],
                [2, 2, 2]
            ],
            "output": [
                [2, 2, 2],
                [2, 2, 2],
                [2, 2, 2],
            ]
        },
    ]
}

metrics = get_metrics_for_task(task)
print(metrics)
