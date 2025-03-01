import numpy as np

def code_execution(input_grid, expected_output_grid, transform_func):
    """Executes the transformation and provides a detailed comparison."""

    actual_output_grid = transform_func(input_grid)
    is_correct = np.array_equal(np.array(actual_output_grid), np.array(expected_output_grid))
    
    input_grid = np.array(input_grid)
    expected_output_grid = np.array(expected_output_grid)
    actual_output_grid = np.array(actual_output_grid)

    input_orange_cols = np.any(input_grid == 7, axis=0)
    expected_orange_cols = np.any(expected_output_grid == 7, axis=0)
    actual_orange_cols = np.any(actual_output_grid == 7, axis=0)
    
    results = {
        "is_correct": is_correct,
        "input_shape": input_grid.shape,
        "expected_output_shape": expected_output_grid.shape,
        "actual_output_shape": actual_output_grid.shape,
        "input_orange_columns": input_orange_cols.tolist(),
        "expected_output_orange_columns": expected_orange_cols.tolist(),
        "actual_output_orange_columns": actual_orange_cols.tolist(),

    }
    return results