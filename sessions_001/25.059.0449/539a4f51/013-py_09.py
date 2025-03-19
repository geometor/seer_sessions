import numpy as np

def describe_grid(grid):
    """Provides a concise description of a grid."""
    height, width = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.count_nonzero(grid == color) for color in unique_colors}
    return {
        "height": height,
        "width": width,
        "unique_colors": unique_colors.tolist(),
        "color_counts": color_counts
    }

def compare_grids(grid1, grid2):
    """Compares two grids and returns a description of differences."""
    if grid1.shape != grid2.shape:
        return "Different shapes"
    else:
        diff = grid1 != grid2
        diff_coords = np.where(diff)
        num_diffs = np.sum(diff)
        return {
            "num_differences": num_diffs,
            "different_coordinates": list(zip(diff_coords[0].tolist(), diff_coords[1].tolist())),
            "grid1_values_at_diff": grid1[diff].tolist(),
            "grid2_values_at_diff": grid2[diff].tolist(),
        }
train_examples = [
    {
        "input": np.array([[6, 1, 1], [1, 1, 8], [1, 8, 1]]),
        "output": np.array([[6, 1, 1, 6, 1, 1], [1, 1, 8, 1, 1, 8], [1, 8, 1, 1, 8, 1], [6, 1, 1, 6, 1, 1], [1, 1, 8, 1, 1, 8], [1, 8, 1, 1, 8, 1]])
    },
    {
        "input": np.array([[0, 7, 7, 7, 0], [7, 7, 0, 7, 7], [7, 0, 7, 7, 7]]),
        "output": np.array([[0, 7, 7, 7, 0, 0, 7, 7, 7, 0], [7, 7, 0, 7, 7, 7, 7, 0, 7, 7], [7, 0, 7, 7, 7, 7, 0, 7, 7, 7], [0, 7, 7, 7, 0, 0, 7, 7, 7, 0], [7, 7, 0, 7, 7, 7, 7, 0, 7, 7], [7, 0, 7, 7, 7, 7, 0, 7, 7, 7]])
    },
    {
        "input": np.array([[5, 0, 5], [0, 5, 0], [5, 0, 5]]),
        "output": np.array([[5, 0, 5, 5, 0, 5], [0, 5, 0, 0, 5, 0], [5, 0, 5, 5, 0, 5], [5, 0, 5, 5, 0, 5], [0, 5, 0, 0, 5, 0], [5, 0, 5, 5, 0, 5]])
    },
    {
        "input": np.array([[4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4]]),
        "output": np.array([[4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4]])
    }
]

results = []
for i, example in enumerate(train_examples):
    input_grid = example['input']
    expected_output_grid = example['output']
    actual_output_grid = transform(input_grid)
    comparison = compare_grids(expected_output_grid, actual_output_grid)
    results.append({
        "example": i + 1,
        "input_description": describe_grid(input_grid),
        "expected_output_description": describe_grid(expected_output_grid),
        "actual_output_description": describe_grid(actual_output_grid),
        "comparison": comparison
    })

for result in results:
    print(result)