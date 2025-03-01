import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of valid neighbors (up, down, left, right) for a given cell.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors

def is_surrounded_by_black(grid, row, col):
    """
    Checks if a cell is surrounded by black (0) pixels on all four sides.
    """
    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        if grid[r, c] != 0:
            return False
    return True

def transform(input_grid):
    # initialize output_grid as copy of input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # loop for pixels in input and apply expansion rule
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] != 1:
                # Check Black Background rule first
                if is_surrounded_by_black(input_grid, r, c):
                    continue # Remain unchanged

                neighbors = get_neighbors(input_grid, r, c)
                for nr, nc in neighbors:
                    if input_grid[nr, nc] == 1:
                        output_grid[r, c] = 1
                        break  # expand only once

    return output_grid

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a report of the differences.
    """
    if grid1.shape != grid2.shape:
        return "Different shapes: {} vs {}".format(grid1.shape, grid2.shape)
    diff = grid1 != grid2
    if not np.any(diff):
        return "Grids are identical"
    num_diffs = np.sum(diff)
    diff_indices = np.where(diff)
    diff_report = "Number of differences: {}\n".format(num_diffs)
    for i in range(num_diffs):
        row, col = diff_indices[0][i], diff_indices[1][i]
        diff_report += "  Difference at ({}, {}): {} vs {}\n".format(row, col, grid1[row, col], grid2[row,col])
    return diff_report

# Example Inputs and Outputs (from the task)
examples = [
    (np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,0,1,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]),
     np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])),
    
    (np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,1,1,1,1,1,0,0],[0,0,1,0,0,0,1,0,0],[0,0,1,0,0,0,1,0,0],[0,0,1,0,0,0,1,0,0],[0,0,1,1,1,1,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]),
     np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,1,1,1,1,1,0,0],[0,0,1,1,1,1,1,0,0],[0,0,1,1,1,1,1,0,0],[0,0,1,1,1,1,1,0,0],[0,0,1,1,1,1,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]])),

    (np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,1,1,1,1,1,1,1,0],[0,0,1,0,0,0,0,0,1,0],[0,0,1,0,0,0,0,0,1,0],[0,0,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]),
     np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,1,1,1,1,1,1,1,0],[0,0,1,0,0,0,0,0,1,0],[0,0,1,0,0,0,0,0,1,0],[0,0,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])),

     (np.array([[5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5],[5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5],[5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5],[5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5]]),
      np.array([[5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5],[5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5],[5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5],[5,0,5,0,5,0,5,0],[0,5,0,5,0,5,0,5]]))
]

# Run the transformation and compare
for i, (input_grid, expected_output) in enumerate(examples):
    transformed_grid = transform(input_grid)
    comparison_report = compare_grids(transformed_grid, expected_output)
    print(f"Example {i+1}:")
    print(comparison_report)
    print("-" * 20)