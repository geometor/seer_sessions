def compare_grids(grid1, grid2):
    """Counts the number of differing pixels between two grids."""
    return np.sum(grid1 != grid2)

def get_grid_metrics(grid):
  return {
        "rows": grid.shape[0],
        "cols": grid.shape[1],
        "unique_colors": np.unique(grid).tolist(),
    }

def analyze_example(input_grid, expected_output_grid, predicted_output_grid):

    metrics = {
        "input": get_grid_metrics(input_grid),
        "expected_output": get_grid_metrics(expected_output_grid),
        "predicted_output": get_grid_metrics(predicted_output_grid),
        "diff_expected_predicted": compare_grids(expected_output_grid, predicted_output_grid),
    }

    return metrics

# Example Usage (assuming the grids are available - replaced with dummy data)
input_grid = np.array([[1, 4, 1], [4, 4, 4], [1, 4, 1]])  # dummy data
expected_output = np.array([[1, 5, 1], [5, 5, 5], [1, 5, 1]])  # dummy data
predicted_output = transform(input_grid)  # Use the provided transform function

analysis = analyze_example(input_grid, expected_output, predicted_output)
print(analysis)