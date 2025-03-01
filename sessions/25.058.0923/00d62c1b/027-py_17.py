import numpy as np

def analyze_results(input_grid, output_grid, expected_output_grid):
    """
    Analyzes the results and provides metrics.  Returns a dictionary
    of analysis data.
    """
    analysis = {}
    analysis['input_shape'] = input_grid.shape
    analysis['output_shape'] = output_grid.shape
    analysis['expected_output_shape'] = expected_output_grid.shape

    analysis['input_green_count'] = np.sum(input_grid == 3)
    analysis['output_green_count'] = np.sum(output_grid == 3)
    analysis['expected_output_green_count'] = np.sum(expected_output_grid == 3)
     
    analysis['input_yellow_count'] = np.sum(input_grid == 4)
    analysis['output_yellow_count'] = np.sum(output_grid == 4)
    analysis['expected_output_yellow_count'] = np.sum(expected_output_grid == 4)
    
    analysis['correct_pixels'] = np.sum(output_grid == expected_output_grid)
    analysis['total_pixels'] = output_grid.size
    analysis['accuracy'] = analysis['correct_pixels'] / analysis['total_pixels']
    
    return analysis

# Example Usage (replace with actual data for each example)
# Assuming you have loaded: input_grid, output_grid, expected_output_grid
# results = analyze_results(input_grid, output_grid, expected_output_grid)
# print(results)