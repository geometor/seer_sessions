import numpy as np

def analyze_results(input_grid, expected_output, actual_output):
    report = {}

    # Basic grid information
    report['input_shape'] = input_grid.shape
    report['output_shape'] = expected_output.shape
    report['actual_output_shape'] = actual_output.shape

    # Color counts
    report['input_colors'] = np.unique(input_grid, return_counts=True)
    report['output_colors'] = np.unique(expected_output, return_counts=True)
    report['actual_output_colors'] = np.unique(actual_output, return_counts=True)
    
    # check where the grids are different
    report['diff'] = np.where(expected_output != actual_output)

    return report
# example use - simulate an ARC task
example_input_grid = np.array([[0,0,4],[0,4,4],[4,4,4]])
example_expected_output = np.array([[6,0,4],[0,4,4],[4,4,4]])
example_actual_output = transform(example_input_grid)
report = analyze_results(example_input_grid, example_expected_output, example_actual_output)

print(report)