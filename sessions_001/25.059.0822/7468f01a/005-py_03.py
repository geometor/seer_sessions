def get_metrics(input_grid, output_grid, expected_output):
    metrics = {}

    metrics['input_dims'] = input_grid.shape
    metrics['output_dims'] = output_grid.shape
    metrics['expected_output_dims'] = expected_output.shape
    metrics['input_red_count'] = np.sum(input_grid == 2)
    metrics['input_azure_count'] = np.sum(input_grid == 8)
    metrics['output_red_count'] = np.sum(output_grid == 2)
    metrics['output_azure_count'] = np.sum(output_grid == 8)
    metrics['expected_output_red_count'] = np.sum(expected_output == 2)
    metrics['expected_output_azure_count'] = np.sum(expected_output == 8)
    metrics['output_bg_color'] = output_grid[0][0] if output_grid.size > 0 else None
    metrics['expected_output_bg_color'] = expected_output[0][0]
    metrics['match'] = np.array_equal(output_grid, expected_output)
    return metrics

# Example usage (assuming input_grid, output_grid, and expected_output are defined)
# You'd loop through all training examples and call this for each

import numpy as np
#dummy data for testing
input_grid = np.array([[0,0,0],[0,1,1],[0,2,2]])
output_grid = np.array([[2,2],[1,1]])
expected_output = np.array([[2,2],[1,1]])

metrics = get_metrics(input_grid, output_grid, expected_output)
print(metrics)
