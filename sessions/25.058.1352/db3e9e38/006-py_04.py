import numpy as np

def analyze_differences(expected, predicted):
    """
    Analyzes the differences between the expected and predicted outputs.
    Calculates metrics like the number of differing pixels and their colors.
    """
    if expected.shape != predicted.shape:
        return "Grids have different shapes", {}

    diff_grid = (expected != predicted).astype(int)
    num_diff_pixels = np.sum(diff_grid)

    diff_pixels_info = {}
    for row in range(expected.shape[0]):
        for col in range(expected.shape[1]):
            if diff_grid[row, col] == 1:
                expected_color = expected[row, col]
                predicted_color = predicted[row, col]
                diff_pixels_info[(row, col)] = (expected_color, predicted_color)

    return num_diff_pixels, diff_pixels_info
# Example data (same as in the provided code)
train_in = []
train_out = []

# Example Task 1
train_in.append(np.array([[0, 0, 7, 0, 0, 0], [0, 0, 7, 0, 7, 0], [7, 7, 7, 7, 7, 7], [0, 0, 7, 0, 7, 0], [0, 0, 7, 0, 0, 0]]))
train_out.append(np.array([[0, 8, 7, 8, 0, 0], [0, 8, 7, 8, 7, 8], [7, 7, 7, 7, 7, 7], [0, 8, 7, 8, 7, 8], [0, 8, 7, 8, 0, 0]]))

# Example Task 2
train_in.append(np.array([[7, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0], [0, 0, 7, 0, 0, 0], [0, 7, 0, 0, 0, 0]]))
train_out.append(np.array([[7, 8, 0, 0, 0, 0], [8, 8, 8, 7, 8, 0], [0, 8, 7, 8, 0, 0], [8, 7, 8, 0, 0, 0]]))

# Example Task 3
train_in.append(np.array([[0, 7, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]))
train_out.append(np.array([[8, 7, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 7, 8, 0], [0, 0, 0, 0, 0, 8, 0, 0]]))

predicted_outputs = [transform(inp) for inp in train_in]

for i, (inp, exp, pred) in enumerate(zip(train_in, train_out, predicted_outputs)):
    num_diff_pixels, diff_pixels_info = analyze_differences(exp, pred)
    print(f"Example {i+1}:")
    print("Number of differing pixels:", num_diff_pixels)
    print("Differing pixels info (row, col): (expected_color, predicted_color)", diff_pixels_info)
    print("-" * 20)