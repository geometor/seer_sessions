import numpy as np

def analyze_example(input_grid, output_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    input_values = np.unique(input_grid)
    output_values = np.unique(output_grid)
    return {
        "input_shape": input_shape,
        "output_shape": output_shape,
        "input_values": input_values.tolist(),
        "output_values": output_values.tolist(),
    }

examples = [
    (np.array([[1]]), np.array([[2, 4, 1], [4, 1, 2], [1, 2, 4]])),
    (np.array([[1, 4], [5, 2]]), np.array([[1, 4, 1, 4], [5, 2, 5, 2], [1, 4, 1, 4], [5, 2, 5, 2]])),
    (np.array([[1, 8, 3], [8, 3, 1], [3, 1, 8]]), np.array([[1, 8, 3, 1, 8, 3], [8, 3, 1, 8, 3, 1], [3, 1, 8, 3, 1, 8], [1, 8, 3, 1, 8, 3], [8, 3, 1, 8, 3, 1], [3, 1, 8, 3, 1, 8]])),
]

analysis_results = [analyze_example(inp, out) for inp, out in examples]
print(analysis_results)
