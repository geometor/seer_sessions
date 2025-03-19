def analyze_example(input_grid, expected_output, actual_output):
    input_array = np.array(input_grid)
    expected_array = np.array(expected_output)
    actual_array = np.array(actual_output)

    input_shapes = set()
    for color in np.unique(input_array):
        coords = np.argwhere(input_array == color)
        if len(coords) > 0:
            min_row, min_col = np.min(coords, axis=0)
            max_row, max_col = np.max(coords, axis=0)
            shape = (max_row - min_row + 1, max_col - min_col + 1)
            input_shapes.add((color, shape))

    expected_shapes = set()
    for color in np.unique(expected_array):
        coords = np.argwhere(expected_array == color)
        if len(coords) > 0:
            min_row, min_col = np.min(coords, axis=0)
            max_row, max_col = np.max(coords, axis=0)
            shape = (max_row - min_row + 1, max_col - min_col + 1)
            expected_shapes.add((color, shape))

    print("Input Grid:")
    print(input_array)
    print("Expected Output:")
    print(expected_array)
    print("Actual Output:")
    print(actual_array)
    print("Input Shapes (color, (height, width)):", input_shapes)
    print("Expected Shapes (color, (height, width)):", expected_shapes)
    print("Match:", np.array_equal(expected_array, actual_array))
    print("---")

# Example data (replace with actual data from the task)
examples = [
    (
        [[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8]],
        [[8, 8, 8], [8, 8, 8], [8, 8, 8]],
        [[8, 8, 8], [8, 8, 8], [8, 8, 8]]
    ),
    (
        [[8, 8, 8, 8, 8, 8, 8, 8], [8, 5, 5, 5, 8, 8, 8, 8], [8, 5, 5, 5, 8, 8, 8, 8], [8, 5, 5, 5, 8, 8, 8, 8], [8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 0, 0, 0], [8, 8, 8, 8, 8, 0, 0, 0]],
        [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
        [[8, 8, 8], [8, 5, 5], [8, 5, 5]]
    ),
        (
        [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0], [0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0], [0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0], [0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0], [0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    ),
    (
         [[4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
        [[4, 4, 4], [4, 4, 4], [4, 4, 4]]
    )
]


for input_grid, expected_output, actual_output in examples:
    analyze_example(input_grid, expected_output, actual_output)
