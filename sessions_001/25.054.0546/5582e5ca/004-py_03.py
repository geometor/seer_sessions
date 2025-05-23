import numpy as np
from collections import Counter

def analyze_example(input_grid, expected_output, transformed_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    transformed_output = np.array(transformed_output)


    input_colors = Counter(input_grid.flatten())
    expected_colors = Counter(expected_output.flatten())
    transformed_colors = Counter(transformed_output.flatten())

    print(f"  Input Colors: {input_colors}")
    print(f"  Expected Colors: {expected_colors}")
    print(f"  Transformed Colors: {transformed_colors}")

    #Additional metrics that could be helpful
    input_shape = input_grid.shape
    print(f" Input Shape: {input_shape}")
    #mode color, color location

print("Example 1:")
analyze_example(
    [[4, 4, 8], [6, 4, 3], [6, 3, 0]],
    [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
    [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
)

print("\nExample 2:")
analyze_example(
    [[6, 8, 9], [1, 8, 1], [9, 4, 9]],
    [[9, 9, 9], [9, 9, 9], [9, 9, 9]],
    [[6, 6, 6], [6, 6, 6], [6, 6, 6]],
)

print("\nExample 3:")
analyze_example(
    [[4, 6, 9], [6, 4, 1], [8, 8, 6]],
    [[6, 6, 6], [6, 6, 6], [6, 6, 6]],
    [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
)