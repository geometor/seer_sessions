# Simulated Code Execution and Reporting (using provided example data)
import numpy as np

def compare_grids(predicted, expected):
    """Simple comparison, could use more robust metrics."""
    return np.array_equal(predicted, expected)

train_pairs = [
    (np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]]), np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]])),
    (np.array([[8, 8, 8, 8, 8, 8, 5, 5, 5], [8, 8, 8, 8, 8, 8, 5, 5, 5], [8, 8, 8, 8, 8, 8, 5, 5, 5], [8, 8, 8, 8, 8, 8, 5, 5, 5], [8, 8, 8, 8, 8, 8, 5, 5, 5], [8, 8, 8, 8, 8, 8, 5, 5, 5], [5, 5, 5, 8, 8, 8, 5, 5, 5], [5, 5, 5, 8, 8, 8, 5, 5, 5], [5, 5, 5, 8, 8, 8, 5, 5, 5]]), np.array([[8, 8, 5], [8, 8, 5], [5, 8, 5]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 1, 1, 8, 8, 8, 8, 8, 8], [8, 1, 1, 8, 8, 8, 8, 8, 8], [8, 1, 1, 8, 8, 8, 8, 8, 8]]), np.array([[8, 8, 8], [8, 8, 8], [8, 1, 8]]))
]

# Previous transform function (simulated execution)
def transform(input_grid):
    height, width = input_grid.shape
    block_height = height // 3
    block_width = width // 3
    colors = {}
    colors[(0, 0)] = input_grid[block_height // 2, block_width // 2]
    colors[(0, 1)] = input_grid[block_height // 2, block_width + block_width // 2]
    colors[(0, 2)] = input_grid[block_height // 2, 2*block_width + block_width//2]
    colors[(1, 0)] = input_grid[block_height + block_height // 2, block_width // 2]
    colors[(1, 1)] = input_grid[height // 2, width // 2]
    colors[(1, 2)] = input_grid[block_height + block_height//2, 2*block_width + block_width//2]
    colors[(2, 0)] = input_grid[2*block_height + block_height//2, block_width // 2]
    colors[(2, 1)] = input_grid[2*block_height + block_height//2, block_width + block_width // 2]
    colors[(2, 2)] = input_grid[2*block_height + block_height//2, 2*block_width + block_width//2]
    output_grid = np.zeros((3, 3), dtype=int)
    for (row, col), color in colors.items():
        output_grid[row, col] = color
    return output_grid

results = []
for i, (input_grid, expected_output) in enumerate(train_pairs):
    predicted_output = transform(input_grid)
    is_correct = compare_grids(predicted_output, expected_output)
    results.append({
        "example_index": i + 1,
        "input_shape": input_grid.shape,
        "expected_output_shape": expected_output.shape,
        "predicted_output_shape": predicted_output.shape,
        "is_correct": is_correct,
        "common_colors": list(set(input_grid.flatten()) & set(expected_output.flatten()))
    })

for result in results:
    print(result)
