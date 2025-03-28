import numpy as np

def analyze_example(input_grid, expected_output, transformed_output):
    input_array = np.array(input_grid)
    expected_array = np.array(expected_output)
    transformed_array = np.array(transformed_output)

    input_shape = input_array.shape
    expected_shape = expected_array.shape
    transformed_shape = transformed_array.shape

    correct_pixels = np.sum(transformed_array == expected_array)
    num_pixels_expected = expected_array.size

    if num_pixels_expected > 0:

        pixel_accuracy = (correct_pixels / num_pixels_expected) * 100
    else:
        pixel_accuracy=0

    print(f"  Input Shape: {input_shape}")
    print(f"  Expected Shape: {expected_shape}")
    print(f"  Transformed Shape: {transformed_shape}")
    print(f"  Pixel Accuracy: {pixel_accuracy:.2f}%")
    if expected_array.size > 0:
        print(f"  Pixels Off: {expected_array.size-correct_pixels}")

# Example 1 data
input1 = [
    [1, 1, 3, 2, 1, 1, 3, 2],
    [1, 1, 3, 3, 1, 1, 3, 3],
    [3, 3, 1, 1, 3, 3, 1, 1],
    [2, 3, 1, 1, 2, 3, 1, 1]
]
expected1 = [
    [1, 1, 3, 2],
    [1, 1, 3, 3],
    [3, 3, 1, 1],
    [2, 3, 1, 1]
]
transformed1 = [
    [1, 3, 1, 3],
    [1, 3, 1, 3],
    [3, 1, 3, 1],
    [2, 1, 2, 1]
]

# Example 2 data
input2 = [
    [4, 4, 4, 4, 4, 4],
    [6, 4, 8, 6, 4, 8],
    [6, 6, 8, 6, 6, 8]
]
expected2 = [
    [4, 4, 4],
    [6, 4, 8],
    [6, 6, 8]
]
transformed2 = [
    [4, 4, 4],
    [6, 8, 4],
    [6, 8, 6]
]

# Example 3 data
input3 = [
    [2, 3],
    [3, 2],
    [4, 4],
    [2, 3],
    [3, 2],
    [4, 4]
]
expected3 = [
    [2, 3],
    [3, 2],
    [4, 4]
]
transformed3 = [
    [2],
    [3],
    [4],
    [2],
    [3],
    [4]
]

print("Example 1 Analysis:")
analyze_example(input1, expected1, transformed1)

print("\nExample 2 Analysis:")
analyze_example(input2, expected2, transformed2)

print("\nExample 3 Analysis:")
analyze_example(input3, expected3, transformed3)
