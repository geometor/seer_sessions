def analyze_example(input_grid, output_grid):
    import numpy as np

    input_array = np.array(input_grid)
    output_array = np.array(output_grid)

    input_dims = input_array.shape
    output_dims = output_array.shape

    input_colors = np.unique(input_array)
    output_colors = np.unique(output_array)

    print(f"Input Dimensions: {input_dims}")
    print(f"Output Dimensions: {output_dims}")
    print(f"Input Colors: {input_colors}")
    print(f"Output Colors: {output_colors}")
    print("---")

examples = [
    ([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 1]], [[0, 0, 1], [0, 1, 1]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0, 7, 7], [0, 0, 0, 0, 0, 7, 7, 7]], [[0, 0, 0, 7], [0, 0, 7, 7], [0, 7, 7, 7]]),
    ([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0], [0, 0, 0, 0, 4, 4, 0]], [[0, 0, 4], [0, 4, 4]]),
    ([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0], [0, 0, 5, 5, 0, 0]], [[0, 5], [5, 5]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0, 6, 6, 0], [0, 0, 0, 0, 0, 6, 6, 6, 0]], [[0, 0, 6], [0, 6, 6], [6, 6, 6]])
]

for input_grid, output_grid in examples:
    analyze_example(input_grid, output_grid)
