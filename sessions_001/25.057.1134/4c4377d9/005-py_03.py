def analyze_grid_pair(input_grid, output_grid):
    """
    Analyzes an input and output grid pair, reporting on their shapes and unique colors.

    Args:
        input_grid (list of lists): The input grid.
        output_grid (list of lists): The output grid.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    import numpy as np

    input_array = np.array(input_grid)
    output_array = np.array(output_grid)

    input_shape = input_array.shape
    output_shape = output_array.shape
    input_colors = np.unique(input_array).tolist()
    output_colors = np.unique(output_array).tolist()

    return {
        "input_shape": input_shape,
        "output_shape": output_shape,
        "input_colors": input_colors,
        "output_colors": output_colors,
    }

# example usage - replace with actual grids from the task data
# example_data = [
#     ([[1, 1], [1, 1]], [[1, 1], [1, 1], [1, 1], [1, 1]]), #example 1, success
#     ([[4, 4, 4], [4, 5, 4], [4, 4, 4]], [[4, 4, 4, 4, 4, 4], [4, 5, 5, 5, 5, 4], [4, 4, 4, 4, 4, 4]]), #example 2, failure
#     ([[2, 2, 2, 2], [2, 8, 8, 2], [2, 8, 8, 2], [2, 2, 2, 2]], [[2, 8, 8, 2], [2, 8, 8, 2]]), #example 3, failure

# ]
example_data = [
    ([[1, 1], [1, 1]], [[1, 1], [1, 1], [1, 1], [1, 1]]),
    ([[4, 4, 4], [4, 5, 4], [4, 4, 4]], [[4, 4, 4, 4, 4, 4], [4, 5, 5, 5, 5, 4], [4, 4, 4, 4, 4, 4]]),
    ([[2, 2, 2, 2], [2, 8, 8, 2], [2, 8, 8, 2], [2, 2, 2, 2]], [[2, 8, 8, 2], [2, 8, 8, 2]]),
]
results = [analyze_grid_pair(inp, out) for inp, out in example_data]
print(results)

