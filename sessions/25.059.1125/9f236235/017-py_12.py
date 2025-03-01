def code_execution(input_grid, expected_output, actual_output):
    """Executes code to gather metrics about the input, expected output, and actual output."""

    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    input_shape = input_grid.shape
    input_unique_colors = np.unique(input_grid)
    expected_shape = expected_output.shape
    expected_unique_colors = np.unique(expected_output)
    actual_shape = actual_output.shape
    actual_unique_colors = np.unique(actual_output)
    correct = np.array_equal(expected_output,actual_output)
    
    regions = find_regions(input_grid)
    
    num_regions = len(regions)

    print(f"  Input Shape: {input_shape}")
    print(f"  Input Unique Colors: {input_unique_colors}")
    print(f"  Number of Regions: {num_regions}")
    print(f"  Expected Output Shape: {expected_shape}")
    print(f"  Expected Unique Colors: {expected_unique_colors}")
    print(f"  Actual Output Shape: {actual_shape}")
    print(f"  Actual Unique Colors: {actual_unique_colors}")
    print(f"  Correct: {correct}")
    print(f"Regions:")
    for color, pixels in regions.items():
        print(f"    Color {color}: {pixels}")


examples = [
    (
        [[3, 3, 3, 1, 1, 1, 1, 1, 8, 8, 8],
         [3, 3, 3, 1, 1, 1, 1, 1, 8, 8, 8],
         [3, 3, 3, 1, 1, 1, 1, 1, 8, 8, 8],
         [2, 2, 2, 1, 1, 1, 1, 1, 8, 8, 8],
         [2, 2, 2, 1, 1, 1, 1, 1, 8, 8, 8],
         [2, 2, 2, 1, 1, 1, 1, 1, 8, 8, 8],
         [2, 2, 2, 1, 1, 1, 1, 1, 8, 8, 8],
         [2, 2, 2, 1, 1, 1, 1, 1, 8, 8, 8],
         [2, 2, 2, 1, 1, 1, 1, 1, 4, 4, 4],
         [2, 2, 2, 1, 1, 1, 1, 1, 4, 4, 4],
         [2, 2, 2, 1, 1, 1, 1, 1, 4, 4, 4]],
        [[0, 8, 8],
         [0, 8, 8],
         [2, 0, 0]],
        [[0, 8, 8],
         [0, 8, 8],
         [4, 0, 0]]
    ),
    (
        [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
         [3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
         [3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
         [9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0],
         [9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0],
         [9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0],
         [9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0]],
        [[3, 0, 0],
         [3, 0, 0],
         [0, 0, 0]],
        [[3, 0, 0],
         [3, 0, 0],
         [0, 0, 0]]
    ),
    (
       [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
        [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8]],
        [[0, 8, 8],
         [0, 8, 8],
         [0, 8, 8]],
        [[0, 8, 8],
         [0, 8, 8],
         [8, 0, 0]]
    ),
        (
       [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5],
        [3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5],
        [3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5],
        [3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5],
        [3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5],
        [3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5],
        [3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5]],
        [[3, 5, 5],
         [3, 5, 5],
         [3, 5, 5]],
        [[3, 5, 5],
         [3, 5, 5],
         [5, 0, 0]]
    )

]

for i, (input_grid, expected_output, actual_output) in enumerate(examples):
    print(f"Example {i+1}:")
    code_execution(input_grid, expected_output, actual_output)
    print("-" * 20)