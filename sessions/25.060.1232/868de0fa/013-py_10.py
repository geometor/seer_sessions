import numpy as np

def compare_grids(grid1, grid2):
    """Checks if two grids are identical."""
    return np.array_equal(grid1, grid2)

def analyze_results(task_examples, transform_function):
    """Analyzes the transformation results for a set of examples.
       Prints relevant information to understand the discrepancies.
    """
    results = []
    for i, (input_grid, expected_output)grid) in enumerate(task_examples):

        #convert grids to numpy arrays.
        input_grid = np.array(input_grid)
        expected_output_grid = np.array(expected_output_grid)

        actual_output_grid = transform_function(input_grid)
        grids_equal = compare_grids(expected_output_grid, actual_output_grid)

        # Find blue regions
        blue_region_input = find_contiguous_region(input_grid, 1)
        blue_region_expected = find_contiguous_region(expected_output_grid, 1)
        blue_region_actual = find_contiguous_region(actual_output_grid, 1)

        # Find other regions
        red_region_expected = find_contiguous_region(expected_output_grid, 2)
        red_region_actual = find_contiguous_region(actual_output_grid, 2)
        orange_region_expected = find_contiguous_region(expected_output_grid, 7)
        orange_region_actual = find_contiguous_region(actual_output_grid, 7)
        gray_region_input = find_contiguous_region(input_grid, 5)
        gray_region_expected = find_contiguous_region(expected_output_grid, 5)


        results.append({
            "example_number": i + 1,
            "grids_equal": grids_equal,
            "input_grid_shape": input_grid.shape,
            "output_grid_shape": expected_output_grid.shape,
            "blue_region_input_size": len(blue_region_input),
            "blue_region_expected_size": len(blue_region_expected),
            "blue_region_actual_size": len(blue_region_actual),
            "red_region_expected_size": len(red_region_expected),
            "red_region_actual_size": len(red_region_actual),
            "orange_region_expected_size": len(orange_region_expected),
            "orange_region_actual_size": len(orange_region_actual),
            "gray_region_input_size": len(gray_region_input),
            "gray_region_expected_size": len(gray_region_expected),
        })

    for result in results:
        print(result)

# Example usage (assuming 'task' variable holds the ARC task data)
# Load the task
from load_task import load_task
task = load_task('7b601.json', train_mode=True)
analyze_results(task['train'], transform)