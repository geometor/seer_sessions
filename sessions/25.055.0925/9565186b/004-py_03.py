import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a detailed report."""
    if grid1.shape != grid2.shape:
        return "Grids have different dimensions"

    matching_cells = np.sum(grid1 == grid2)
    mismatching_cells = grid1.size - matching_cells
    mismatches = []

    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i, j] != grid2[i, j]:
                mismatches.append({
                    'row': i,
                    'col': j,
                    'grid1_value': grid1[i, j],
                    'grid2_value': grid2[i, j]
                })

    report = {
        'matching_cells': matching_cells,
        'mismatching_cells': mismatching_cells,
        'mismatches': mismatches
    }
    return report

# Example Input/Output grids from the task
input_grid1 = np.array([[1, 2, 8], [2, 1, 1]])
expected_output1 = np.array([[5, 2, 5], [2, 5, 5]])

input_grid2 = np.array([[8,8],[1,1]])
expected_output2 = np.array([[5,5],[5,5]])

input_grid3 = np.array([[8,1,2],[2,2,8]])
expected_output3 = np.array([[5,5,2],[2,2,5]])


def analyze_example(input_grid, expected_output):
    """Analyzes a single example and provides observations."""

    # Basic stats
    num_rows = input_grid.shape[0]
    num_cols = input_grid.shape[1]
    unique_input_colors = np.unique(input_grid)
    unique_output_colors = np.unique(expected_output)

    report = compare_grids(input_grid, expected_output)

    print(f"  Dimensions: {num_rows}x{num_cols}")
    print(f"  Unique Input Colors: {unique_input_colors}")
    print(f"  Unique Output Colors: {unique_output_colors}")
    print(f"Comparison report: {report}")
    print("-----")


print("Example 1 Analysis:")
analyze_example(input_grid1, expected_output1)

print("Example 2 Analysis:")
analyze_example(input_grid2, expected_output2)

print("Example 3 Analysis:")
analyze_example(input_grid3, expected_output3)