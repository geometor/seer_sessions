import numpy as np

# ... (Previous Code: transform, find_cluster, etc.) ...
def calculate_metrics(input_grid, output_grid, predicted_output_grid):
    """Calculates metrics comparing the predicted output to the actual output."""
    match = np.array_equal(output_grid, predicted_output_grid)
    diff = None
    if not match:
        diff = output_grid - predicted_output_grid
    
    input_colors = set(np.unique(input_grid).tolist())
    output_colors = set(np.unique(output_grid).tolist())
    predicted_output_colors = set(np.unique(predicted_output_grid).tolist())
    
    metrics = {
      "match": match,
      "input_colors": input_colors,
      "output_colors": output_colors,
      "predicted_output_colors": predicted_output_colors,
      "diff": diff
    }
    
    return metrics

# Example Usage (assuming train_input_0, train_output_0, etc. are defined):
train_examples = [
    (train_input_0, train_output_0),
    (train_input_1, train_output_1),
    (train_input_2, train_output_2),
    (train_input_3, train_output_3),
    (train_input_4, train_output_4),
]

results = []

for i, (input_grid, output_grid) in enumerate(train_examples):
    predicted_output_grid = transform(input_grid.copy())
    metrics = calculate_metrics(input_grid, output_grid, predicted_output_grid)
    results.append(
        {
            "example": i,
            "metrics": metrics
        }
    )

import json
print(json.dumps(results, indent=2))
