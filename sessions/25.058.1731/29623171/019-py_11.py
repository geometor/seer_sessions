import numpy as np

def code_execution(input_grid, output_grid, predicted_output):
    """
    Analyzes the input, expected output, and actual output grids.
    Provides metrics.
    """

    def count_pixels(grid, color):
        return np.sum(grid == color)
    
    metrics = {}
    
    metrics["input_green"] = count_pixels(input_grid, 3)
    metrics["output_green"] = count_pixels(output_grid, 3)
    metrics["predicted_green"] = count_pixels(predicted_output, 3)

    metrics["input_gray"] = count_pixels(input_grid, 5)
    metrics["output_gray"] = count_pixels(output_grid, 5)
    metrics["predicted_gray"] = count_pixels(predicted_output, 5)

    metrics["diff_output_predicted_green"] = np.sum(output_grid - predicted_output == 3)
    metrics["diff_predicted_output_green"] = np.sum(predicted_output - output_grid == 3)

    return metrics