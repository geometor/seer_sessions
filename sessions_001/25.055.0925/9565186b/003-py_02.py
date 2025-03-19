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

# Example Input/Output grids from the task (replace with actual data)
input_grid1 = np.array([[1, 2, 8], [2, 1, 1]])
expected_output1 = np.array([[5, 2, 5], [2, 5, 5]])

input_grid2 = np.array([[8,8],[1,1]])
expected_output2 = np.array([[5,5],[5,5]])

input_grid3 = np.array([[8,1,2],[2,2,8]])
expected_output3 = np.array([[5,5,2],[2,2,5]])

# Test the provided transform function (replace with actual transform function)
def transform(input_grid):
    output_grid = np.copy(input_grid)
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 1 or output_grid[i, j] == 8:
                output_grid[i, j] = 5
    return output_grid

predicted_output1 = transform(input_grid1)
predicted_output2 = transform(input_grid2)
predicted_output3 = transform(input_grid3)

# Generate comparison reports
report1 = compare_grids(predicted_output1, expected_output1)
report2 = compare_grids(predicted_output2, expected_output2)
report3 = compare_grids(predicted_output3, expected_output3)

print("Report 1:")
print(report1)
print("\nReport 2:")
print(report2)
print("\nReport 3:")
print(report3)