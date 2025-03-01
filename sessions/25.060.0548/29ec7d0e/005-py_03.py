import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    """Analyzes a single example and gathers metrics."""

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_grid = np.array(predicted_grid)

    metrics = {}

    # Check if the prediction is correct
    metrics['correct'] = np.array_equal(output_grid, predicted_grid)

    # Count of '0' cells in the input
    metrics['input_zero_count'] = np.sum(input_grid == 0)

    # Count of '0' cells in the output
    metrics['output_zero_count'] = np.sum(output_grid == 0)

    #check to see if shapes are the same
    metrics['same_shape'] = input_grid.shape == output_grid.shape

    # Calculate the difference grid.
    metrics['difference'] = output_grid - input_grid

    return metrics