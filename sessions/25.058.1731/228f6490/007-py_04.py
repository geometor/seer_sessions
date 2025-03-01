import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns differences."""
    if grid1.shape != grid2.shape:
        return "Different Shapes"
    else:
        diff = grid1 != grid2
        return np.sum(diff)  # Returns number of differing pixels.

def find_pixels(grid, color):
    """Finds coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

# Example Input/Output/Predicted Grids (replace with actual data from the task)
train_ex_inputs = [
    np.array([[8, 1, 1, 1, 1, 1, 1, 1, 1, 6], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [6, 1, 1, 1, 1, 1, 1, 1, 1, 8]]),
    np.array([[8, 0, 8, 8, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 0, 5, 0, 5, 0, 0, 0, 0], [6, 6, 0, 6, 0, 0, 0, 0, 0, 0]]),
    np.array([[8, 1, 8, 1, 8, 1, 8, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 6, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 6, 1, 1]])
]

train_ex_outputs = [
    np.array([[6, 1, 1, 1, 1, 1, 1, 1, 1, 8], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [8, 1, 1, 1, 1, 1, 1, 1, 1, 6]]),
    np.array([[6, 0, 6, 6, 6, 6, 6, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 5, 5], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 0, 5, 0, 5, 0, 0, 0, 0], [8, 8, 0, 8, 0, 0, 0, 0, 0, 0]]),
    np.array([[6, 1, 6, 1, 6, 1, 6, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 8, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 8, 1, 1]])
]

results = []
for i, (input_grid, expected_output) in enumerate(zip(train_ex_inputs, train_ex_outputs)):
    predicted_output = transform(input_grid)  # Using the provided transform function
    diff_count = compare_grids(predicted_output, expected_output)
    results.append(diff_count)
    azure_count = np.sum(input_grid == 8)
    magenta_count = np.sum(input_grid == 6)

    print(f"Example {i+1}:")
    print(f"  Azure Pixels (Input): {azure_count}")
    print(f"  Magenta Pixels (Input): {magenta_count}")
    print(f"  Differences between predicted and expected: {diff_count}")

print(results)