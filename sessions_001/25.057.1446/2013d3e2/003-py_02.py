import numpy as np

def code_execution(input_grid, output_grid, predicted_grid):
    """
    Provides metrics to compare input, output, and prediction grids.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_grid = np.array(predicted_grid)

    input_nonzero_count = np.count_nonzero(input_grid)
    output_nonzero_count = np.count_nonzero(output_grid)
    predicted_nonzero_count = np.count_nonzero(predicted_grid)

    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    predicted_colors = np.unique(predicted_grid)
    
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    predicted_shape = predicted_grid.shape

    # Check if prediction matches output
    match = np.array_equal(output_grid, predicted_grid)

    return {
        "input_nonzero_count": input_nonzero_count,
        "output_nonzero_count": output_nonzero_count,
        "predicted_nonzero_count": predicted_nonzero_count,
        "input_colors": input_colors.tolist(),
        "output_colors": output_colors.tolist(),
        "predicted_colors": predicted_colors.tolist(),
        "input_shape": input_shape,
        "output_shape": output_shape,
        "predicted_shape": predicted_shape,
        "match": match
    }