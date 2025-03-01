import numpy as np

def analyze_grid(grid, grid_name):
    """Analyzes a single grid and returns relevant metrics."""
    rows, cols = grid.shape
    non_zero_count = np.count_nonzero(grid)
    unique_colors = np.unique(grid)
    zero_count = (grid == 0).sum()

    print(f"--- {grid_name} Analysis ---")
    print(f"  Dimensions: {rows}x{cols}")
    print(f"  Non-zero Pixels: {non_zero_count}")
    print(f"  Zero Pixels: {zero_count}")
    print(f"  Unique Colors: {unique_colors}")

def compare_grids(input_grid, output_grid, predicted_grid):
    """Compares the output and predicted grids, highlighting discrepancies."""
    if output_grid.shape != predicted_grid.shape:
        print("  ERROR: Output and Predicted grids have different shapes.")
        return

    diff = output_grid != predicted_grid
    num_diffs = np.sum(diff)

    print(f"  Differences between Output and Predicted: {num_diffs} pixels")
    if num_diffs > 0:
      print(f"  Coordinates of Differences: {list(zip(*np.where(diff)))}")


#Example grids provided below - using the ones from prompt

input_grid_1 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 3, 0],
])

output_grid_1 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
])

input_grid_2 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

output_grid_2 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

input_grid_3 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
])

output_grid_3 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

# Previous transform function (from the prompt)
def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # get dimensions
    rows, cols = input_grid.shape

    # Preserve Zeroes:  Iterate through all cells
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0:
                output_grid[i, j] = 0  # Keep 0s in place
            else:
                output_grid[i,j] = 0


    # Mirror, Top to Bottom
    for j in range(cols):
        output_grid[rows - 1, j] = input_grid[0, j]

    # Mirror, Left to Right
    for i in range(rows):
        output_grid[i, cols-1] = input_grid[i,0]

    return output_grid

predicted_grid_1 = transform(input_grid_1)
predicted_grid_2 = transform(input_grid_2)
predicted_grid_3 = transform(input_grid_3)

analyze_grid(input_grid_1, "Input Grid 1")
analyze_grid(output_grid_1, "Output Grid 1")
analyze_grid(predicted_grid_1, "Predicted Grid 1")
compare_grids(input_grid_1, output_grid_1, predicted_grid_1)
print()

analyze_grid(input_grid_2, "Input Grid 2")
analyze_grid(output_grid_2, "Output Grid 2")
analyze_grid(predicted_grid_2, "Predicted Grid 2")
compare_grids(input_grid_2, output_grid_2, predicted_grid_2)
print()

analyze_grid(input_grid_3, "Input Grid 3")
analyze_grid(output_grid_3, "Output Grid 3")
analyze_grid(predicted_grid_3, "Predicted Grid 3")
compare_grids(input_grid_3, output_grid_3, predicted_grid_3)