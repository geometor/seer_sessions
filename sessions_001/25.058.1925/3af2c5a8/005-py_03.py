import numpy as np

def get_grid_properties(grid):
    """Returns properties of the grid."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    return {
        'rows': rows,
        'cols': cols,
        'unique_colors': unique_colors.tolist(),
        'color_counts': color_counts,
    }

def compare_grids(grid1, grid2):
    """Compares two grids and returns a diff."""
    if grid1.shape != grid2.shape:
        return "Shapes are different"
    else:
        diff = grid1 != grid2
        num_diffs = np.sum(diff)
        return {
            'num_diffs': num_diffs,
            'diff_positions': np.argwhere(diff).tolist(),
        }
    
# Example data (replace with your actual data)
train_examples = [
    {
        'input': np.array([[8, 1, 8, 1], [1, 8, 1, 8], [8, 1, 8, 1]]),
        'output': np.array([[8, 8, 1, 1, 8, 8, 1, 1], [8, 8, 1, 1, 8, 8, 1, 1], [1, 1, 8, 8, 1, 1, 8, 8], [1, 1, 8, 8, 1, 1, 8, 8], [8, 8, 1, 1, 8, 8, 1, 1], [8, 8, 1, 1, 8, 8, 1, 1]])
    },
    {
        'input': np.array([[8, 1, 1, 8, 1], [8, 8, 1, 8, 8], [1, 8, 8, 8, 1]]),
        'output': np.array([[8, 8, 1, 1, 1, 1, 8, 8, 1, 1], [8, 8, 8, 8, 1, 1, 8, 8, 8, 8], [8, 8, 8, 8, 1, 1, 8, 8, 8, 8], [1, 1, 8, 8, 8, 8, 8, 8, 1, 1], [1, 1, 8, 8, 8, 8, 8, 8, 1, 1], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
    },
    {
        'input': np.array([[8, 8, 8, 1], [8, 8, 1, 8], [8, 1, 8, 8], [1, 8, 8, 8]]),
        'output': np.array([[8, 8, 8, 8, 8, 8, 1, 1], [8, 8, 8, 8, 8, 8, 1, 1], [8, 8, 8, 8, 1, 1, 8, 8], [8, 8, 8, 8, 1, 1, 8, 8], [8, 8, 1, 1, 8, 8, 8, 8], [8, 8, 1, 1, 8, 8, 8, 8], [1, 1, 8, 8, 8, 8, 8, 8], [1, 1, 8, 8, 8, 8, 8, 8]])
    }
]
results = [
        np.array([[8, 8, 1, 1, 8, 8, 1, 1], [8, 8, 1, 1, 8, 8, 1, 1], [1, 1, 8, 8, 1, 1, 8, 8], [1, 1, 8, 8, 1, 1, 8, 8], [8, 8, 1, 1, 8, 8, 1, 1], [8, 8, 1, 1, 8, 8, 1, 1]]),
        np.array([[8, 8, 1, 1, 1, 8, 8, 8, 1, 1], [8, 8, 8, 1, 1, 8, 8, 8, 8, 1], [8, 8, 8, 1, 1, 8, 8, 8, 8, 1], [1, 1, 8, 8, 8, 8, 8, 8, 8, 1], [1, 1, 8, 8, 8, 8, 8, 8, 8, 1], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        np.array([[8, 8, 8, 8, 8, 8, 1, 1], [8, 8, 8, 8, 8, 1, 8, 8], [8, 8, 8, 8, 1, 8, 8, 8], [8, 8, 1, 1, 8, 8, 8, 8], [8, 8, 1, 8, 8, 8, 8, 8], [1, 1, 8, 8, 8, 8, 8, 8]])
]

for i, example in enumerate(train_examples):
    input_props = get_grid_properties(example['input'])
    output_props = get_grid_properties(example['output'])
    result_props = get_grid_properties(results[i])
    diff = compare_grids(example['output'], results[i])
    print(f"Example {i+1}:")
    print(f"  Input: {input_props}")
    print(f"  Output: {output_props}")
    print(f"Results: {result_props}")
    print(f"  Diff: {diff}")
    print("-" * 20)
