import numpy as np

def code_execution(input_grid, output_grid, predicted_output):
    """
    return metrics about the grids to understand the transformation
    """
    def get_bounding_box(grid, color):
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            return None  # Handle cases with no matching color
        min_row, min_col = coords.min(axis=0)
        max_row, max_col = coords.max(axis=0)
        return (min_row, min_col, max_row, max_col)
    
    results = {}

    # Get Bounding Box of largest blue region.
    input_blue_bbox = get_bounding_box(input_grid, 1)
    results['input_blue_bbox'] = input_blue_bbox

    # output_grid dimensions.
    results['output_grid_shape'] = output_grid.shape if output_grid is not None else None
    
    # predicted_output dimensions.
    results['predicted_output_shape'] = predicted_output.shape if predicted_output is not None else None

    # Check if predicted output matches actual output
    results['match'] = np.array_equal(output_grid, predicted_output)
    
    return results