import numpy as np

def analyze_grid_transform(input_grid, output_grid):
    """Analyzes the transformation between input and output grids.

    Args:
        input_grid: The input grid as a NumPy array.
        output_grid: The output grid as a NumPy array.

    Returns:
        A dictionary containing analysis results.
    """

    analysis = {}

    # Input analysis
    input_non_zero = np.argwhere(input_grid != 0)
    analysis['input_non_zero_count'] = len(input_non_zero)
    analysis['input_non_zero_positions'] = input_non_zero.tolist()
    analysis['input_non_zero_values'] = [input_grid[pos[0], pos[1]] for pos in input_non_zero]

    # Output analysis
    output_non_zero = np.argwhere(output_grid != 0)
    analysis['output_non_zero_count'] = len(output_non_zero)
    analysis['output_non_zero_positions'] = output_non_zero.tolist()
    analysis['output_non_zero_values'] = [output_grid[pos[0], pos[1]] for pos in output_non_zero]

    return analysis

# Example Usage (replace with actual input/output pairs)
input_grid1 = np.array([[0, 0, 0], [0, 5, 0], [0, 0, 0]])
output_grid1 = np.array([[0, 0, 0], [0, 0, 0], [0, 5, 0]])

input_grid2 = np.array([[0, 0, 8, 0], [0, 0, 0, 0], [0, 5, 0, 0], [0, 0, 0, 0]])
output_grid2 = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 8, 0], [0, 5, 0, 0]])

input_grid3 = np.array([[7, 0, 0, 0], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 6, 2]])
output_grid3 = np.array([[7, 0, 0, 0], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 6, 2]])

analysis1 = analyze_grid_transform(input_grid1, output_grid1)
analysis2 = analyze_grid_transform(input_grid2, output_grid2)
analysis3 = analyze_grid_transform(input_grid3, output_grid3)

print("Analysis 1:", analysis1)
print("Analysis 2:", analysis2)
print("Analysis 3:", analysis3)