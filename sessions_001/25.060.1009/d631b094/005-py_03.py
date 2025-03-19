def analyze_example(input_grid, expected_output_grid):
    import numpy as np
    input_grid = np.array(input_grid)
    expected_output_grid = np.array(expected_output_grid)

    blue_count_input = np.count_nonzero(input_grid == 1)
    other_colors_input = set(input_grid.flatten()) - {1}
    output_shape = expected_output_grid.shape
    output_colors = set(expected_output_grid.flatten())

    result = {
        "blue_count_input": blue_count_input,
        "other_colors_input": list(other_colors_input),
        "output_shape": output_shape,
        "output_colors": list(output_colors),
    }
    return result

examples = [
    ([[1, 1], [2, 2]], [[1, 1]]),  # Correct
    ([[0, 1, 0], [1, 0, 1], [0, 1, 0]], [[1, 1, 1, 1]]), # Correct
    ([[5, 5, 5, 5], [5, 1, 5, 1], [5, 5, 5, 5]], [[1,1]]), # Correct
    ([[1, 2, 3], [4, 1, 6], [7, 8, 9]], [[1, 1]]), #Correct
    ([[1, 1, 2], [3, 5, 8], [1, 1, 9]], [[1, 1, 1, 1]])  # Correct
]

results = []
for input_grid, expected_output_grid in examples:
    results.append(analyze_example(input_grid, expected_output_grid))

for i, r in enumerate(results):
    print(f"Example {i + 1}:")
    print(r)
