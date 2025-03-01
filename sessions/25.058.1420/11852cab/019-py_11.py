import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    blue_pixel_input = np.argwhere(input_grid == 1)
    blue_pixel_expected = np.argwhere(expected_output == 1)
    blue_pixel_actual = np.argwhere(actual_output == 1)

    yellow_pixels_input = np.argwhere(input_grid == 4)
    yellow_pixels_expected = np.argwhere(expected_output == 4)
    yellow_pixels_actual = np.argwhere(actual_output == 4)
    
    input_shape = input_grid.shape
    expected_shape = expected_output.shape
    actual_shape = actual_output.shape

    # check input and expected
    same = np.array_equal(input_grid, expected_output)
    same_actual = np.array_equal(input_grid, actual_output)

    print(f"  Input shape: {input_shape}, Expected shape: {expected_shape}, Actual shape: {actual_shape}")
    print(f"  Blue pixel (input): {blue_pixel_input}, Blue pixel (expected): {blue_pixel_expected}, Blue pixel (actual): {blue_pixel_actual}")
    print(f"  Yellow pixels (input): {yellow_pixels_input.shape[0]}, Yellow pixels (expected): {yellow_pixels_expected.shape[0]}, Yellow pixels (actual): {yellow_pixels_actual.shape[0]}")
    print(f"  input == expected: {same}, input == actual: {same_actual}")

# Provided examples
train_examples = [
    {
        "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]],
        "output": [[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]],
        "actual": [[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]]
    },
    {
        "input": [[4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4], [4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4], [1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1], [4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4]],
        "output": [[4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4], [4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4], [1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1], [4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4]],
        "actual": [[4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4], [4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4], [1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1], [4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4]]
    },
     {
        "input": [[8, 8, 8, 4, 8, 8, 8], [8, 8, 8, 4, 8, 8, 8], [8, 8, 8, 1, 8, 8, 8], [8, 8, 8, 4, 8, 8, 8], [8, 8, 8, 4, 8, 8, 8]],
        "output": [[8, 8, 8, 4, 8, 8, 8], [8, 8, 8, 4, 8, 8, 8], [8, 8, 8, 1, 8, 8, 8], [8, 8, 8, 4, 8, 8, 8], [8, 8, 8, 4, 8, 8, 8]],
        "actual": [[8, 8, 8, 4, 8, 8, 8], [8, 8, 8, 4, 8, 8, 8], [8, 8, 8, 1, 8, 8, 8], [8, 8, 8, 4, 8, 8, 8], [8, 8, 8, 4, 8, 8, 8]]
    },
    {
        "input": [[4, 4, 1, 4, 4]],
        "output": [[4, 4, 1, 4, 4]],
        "actual": [[4, 4, 1, 4, 4]]
    },
    {
        "input": [[8, 8, 8, 8, 8], [8, 4, 4, 4, 8], [8, 4, 1, 4, 8], [8, 4, 4, 4, 8], [8, 8, 8, 8, 8]],
        "output": [[8, 8, 8, 8, 8], [8, 4, 4, 4, 8], [8, 4, 1, 4, 8], [8, 4, 4, 4, 8], [8, 8, 8, 8, 8]],
       "actual": [[8, 8, 8, 8, 8], [8, 4, 4, 4, 8], [8, 4, 1, 4, 8], [8, 4, 4, 4, 8], [8, 8, 8, 8, 8]]
    },
    {
        "input" : [[8, 4, 8, 8, 8, 8, 8, 8], [8, 4, 8, 8, 8, 8, 8, 8], [8, 1, 8, 8, 8, 8, 8, 8], [8, 4, 8, 8, 8, 8, 8, 8], [8, 4, 8, 8, 8, 8, 8, 8]],
        "output": [[8, 4, 8, 8, 8, 8, 8, 8], [8, 4, 8, 8, 8, 8, 8, 8], [8, 1, 8, 8, 8, 8, 8, 8], [8, 4, 8, 8, 8, 8, 8, 8], [8, 4, 8, 8, 8, 8, 8, 8]],
        "actual": [[8, 4, 8, 8, 8, 8, 8, 8], [8, 4, 8, 8, 8, 8, 8, 8], [8, 1, 8, 8, 8, 8, 8, 8], [8, 4, 8, 8, 8, 8, 8, 8], [8, 4, 8, 8, 8, 8, 8, 8]]
    }
]

for i, example in enumerate(train_examples):
    print(f"Example {i+1}:")
    analyze_example(example["input"], example["output"], example["actual"])
    print("-" * 20)