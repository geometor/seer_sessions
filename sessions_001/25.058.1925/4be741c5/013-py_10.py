import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    input_dims = input_grid.shape
    expected_dims = expected_output.shape
    actual_dims = actual_output.shape

    input_unique_colors = np.unique(input_grid)
    expected_unique_colors = np.unique(expected_output)
    actual_unique_colors = np.unique(actual_output)

    print(f"  Input Dimensions: {input_dims}")
    print(f"  Expected Dimensions: {expected_dims}")
    print(f"  Actual Dimensions: {actual_dims}")
    print(f"  Input Unique Colors: {input_unique_colors}")
    print(f"  Expected Unique Colors: {expected_unique_colors}")
    print(f"  Actual Unique Colors: {actual_unique_colors}")
    print(f"  Matches Expected: {np.array_equal(expected_output, actual_output)}")

examples = [
    (
        [[8, 8, 8, 8, 8, 2, 2, 2, 2, 2, 5, 5, 5]],
        [[8, 2, 5]],
        [[8, 2, 5]],
    ),
    (
        [[3, 0, 3, 3, 3, 3, 0, 3, 3, 3, 3, 0, 3]],
        [[3, 0]],
        [[3, 0, 3, 0, 3]],
    ),
    (
       [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
       [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
       [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
    ),
    (
      [[5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5],
       [1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1],
       [5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5],
       [1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1],
       [5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5]],
       [[5, 1]],
       [[5, 1]]
    ),
    (
       [[8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8],
        [1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1],
        [8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8],
        [1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1],
        [8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8]],
        [[8, 1]],
        [[8,1]]

    )
]

for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(*example)
