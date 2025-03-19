import numpy as np

def get_grid_metrics(grid):
    """
    Calculates metrics for a given grid.
    """
    metrics = {}
    
    # Count of pixels for each color
    for color_value in range(10):  # 0-9
        metrics[f"count_{color_value}"] = np.sum(grid == color_value)
        
    # Number of unique colors
    metrics["unique_colors"] = len(np.unique(grid))

    # Number of non-zero colors
    metrics["non_zero_colors"] = np.sum(np.array([metrics[f"count_{c}"] for c in range(10)]) > 0)
    
    return metrics

# Example Usage (replace with actual input grids)
example_grids = {
    "train_0_input": np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    "train_0_output": np.array([[10]]),
    "train_1_input": np.array([[8, 5, 1, 5, 3, 5, 7, 7, 5],
                               [8, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
    "train_1_output": np.array([[7]]),
    "train_2_input": np.array([[8, 8, 5, 1, 5, 3, 5, 8, 7],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5],
                               [5, 5, 5, 5, 5, 5, 5, 5, 5]]),
     "train_2_output": np.array([[8]]),
     "train_3_input" : np.array([[5, 5, 5, 5, 5, 5],
                                 [5, 5, 5, 5, 5, 5],
                                 [5, 5, 5, 5, 5, 5],
                                 [5, 5, 5, 5, 5, 5],
                                 [5, 5, 5, 5, 5, 5],
                                 [5, 5, 5, 5, 5, 5]]),
     "train_3_output" : np.array([[7]])
}

results = {}
for grid_name, grid in example_grids.items():
    results[grid_name] = get_grid_metrics(grid)

import json
print(json.dumps(results, indent=2))