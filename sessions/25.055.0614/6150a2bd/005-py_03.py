import numpy as np

def analyze_example(input_grid, expected_output, transformed_output):
    input_array = np.array(input_grid)
    expected_array = np.array(expected_output)
    transformed_array = np.array(transformed_output)

    diff = expected_array - transformed_array
    print("Differences (Expected - Transformed):")
    print(diff)

    input_colors = np.unique(input_array)
    expected_colors = np.unique(expected_array)
    transformed_colors = np.unique(transformed_array)
   

    print(f"Input Colors: {input_colors}")
    print(f"Expected Colors: {expected_colors}")
    print(f"Transformed Colors: {transformed_colors}")


print("Example 1:")
analyze_example(
    [[3, 3, 8], [3, 7, 0], [5, 0, 0]],
    [[0, 0, 5], [0, 7, 3], [8, 3, 3]],
    [[3, 3, 5], [3, 7, 0], [8, 0, 0]]
)

print("\nExample 2:")
analyze_example(
    [[5, 5, 2], [1, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 1], [2, 5, 5]],
    [[5, 1, 0], [5, 0, 0], [2, 0, 0]]
)
