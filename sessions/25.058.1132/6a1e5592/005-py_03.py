import numpy as np

def describe_grid(grid):
    """Provides a basic description of the grid."""
    return {
        'shape': grid.shape,
        'unique_colors': np.unique(grid).tolist(),
        'color_counts': {color: np.count_nonzero(grid == color) for color in np.unique(grid)}
    }

def compare_grids(grid1, grid2):
    """Compares two grids and highlights differences."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"
    else:
        diff = grid1 != grid2
        num_diffs = np.sum(diff)
        diff_indices = np.where(diff)
        diff_values_grid1 = grid1[diff_indices]
        diff_values_grid2 = grid2[diff_indices]
        return {
            'num_differences': num_diffs,
            'diff_indices': diff_indices,
            'diff_values_grid1': diff_values_grid1.tolist(),
            'diff_values_grid2': diff_values_grid2.tolist()
        }
examples = [
    {
        'input': np.array([[5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5],
                           [5, 5, 2, 2, 2, 5],
                           [5, 5, 2, 0, 2, 5],
                           [5, 5, 2, 2, 2, 5],
                           [5, 5, 5, 5, 5, 5]]),
        'output': np.array([[0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 2, 0],
                            [0, 0, 2, 1, 2, 0],
                            [0, 0, 2, 2, 2, 0],
                            [0, 0, 0, 0, 0, 0]])
    },
     {
        'input': np.array([[5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 2, 5, 5, 5],
                           [5, 5, 2, 0, 2, 5, 5],
                           [5, 5, 5, 2, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5]]),
        'output': np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 2, 0, 0, 0],
                            [0, 0, 2, 1, 2, 0, 0],
                            [0, 0, 0, 2, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0]])
    },
    {
        'input': np.array([[5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5],
                           [5, 5, 2, 2, 2, 5, 5, 5],
                           [5, 5, 2, 0, 2, 5, 5, 5],
                           [5, 5, 2, 0, 2, 2, 2, 5],
                           [5, 5, 2, 0, 0, 0, 2, 5],
                           [5, 5, 2, 2, 2, 2, 2, 5],
                           [5, 5, 5, 5, 5, 5, 5, 5]]),
        'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 2, 0, 0, 0],
                            [0, 0, 2, 1, 2, 0, 0, 0],
                            [0, 0, 2, 1, 2, 2, 2, 0],
                            [0, 0, 2, 1, 1, 1, 2, 0],
                            [0, 0, 2, 2, 2, 2, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])
    }
]

from previous_code import transform

for i, example in enumerate(examples):
    input_grid = example['input']
    expected_output_grid = example['output']
    predicted_output_grid = transform(input_grid)

    print(f"Example {i+1}:")
    print("Input Grid Description:", describe_grid(input_grid))
    print("Expected Output Grid Description:", describe_grid(expected_output_grid))
    print("Predicted Output Grid Description:", describe_grid(predicted_output_grid))
    print("Comparison Result:", compare_grids(expected_output_grid, predicted_output_grid))
    print("-" * 40)
