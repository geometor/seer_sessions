def get_metrics(input_grid, output_grid, predicted_output):
    """
    Calculates and returns metrics comparing the output and predicted output.

    Args:
        input_grid: The input grid.
        output_grid: The correct output grid.
        predicted_output: The output grid predicted by the transform function.

    Returns:
        A dictionary containing:
        - 'input_shape': Shape of the input grid.
        - 'output_shape': Shape of the output grid.
        - 'predicted_output_shape': Shape of the predicted output.
        - 'output_matches': True if output and predicted output match exactly,
          False otherwise.
        - 'target_color': most common color in input, if a match, else -1
    """
    import numpy as np

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)

    metrics = {
        'input_shape': input_grid.shape,
        'output_shape': output_grid.shape,
        'predicted_output_shape': predicted_output.shape,
        'output_matches': np.array_equal(output_grid, predicted_output),
        'target_color': -1
    }
    
    if metrics['output_matches']:
      # find most frequent color, excluding white (0)
      unique, counts = np.unique(input_grid[input_grid != 0], return_counts=True)
      if (len(counts) > 0):
          metrics['target_color'] = unique[np.argmax(counts)]

    return metrics