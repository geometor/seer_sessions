import numpy as np

def analyze_grid(input_grid, output_grid, expected_grid):
    """Analyzes the transformation of a single grid."""
    rows, cols = input_grid.shape
    correct = np.array_equal(output_grid, expected_grid)
    print(f"  Dimensions: {rows}x{cols}")
    print(f"  Correct: {correct}")
    if not correct:
        diff = output_grid != expected_grid
        diff_indices = np.where(diff)
        print(f"  Differences at (row, col) indices: {list(zip(diff_indices[0], diff_indices[1]))}")
        for r, c in zip(diff_indices[0], diff_indices[1]):
            print(f"   - ({r}, {c}): Output={output_grid[r, c]}, Expected={expected_grid[r, c]}")
        

# Example Input and Output data (replace with actual data)
input_grid = np.array([[0, 3, 0],
                       [3, 0, 3],
                       [0, 3, 0]])
output_grid = np.array([[0, 8, 0],
                        [9, 0, 9],
                        [0, 9, 0]]) # this is correct per the current code
expected_grid = np.array([[0, 8, 0],
                          [9, 0, 9],
                          [0, 9, 0]])


analyze_grid(input_grid,output_grid, expected_grid)

input_grid = np.array([[0, 0, 0],
                       [0, 3, 0],
                       [0, 0, 0]])
output_grid = np.array([[0, 0, 0],
                        [8, 3, 8],
                        [0, 0, 0]]) # current code
expected_grid = np.array([[0, 0, 0],
                          [0, 9, 0],
                          [0, 0, 0]])

analyze_grid(input_grid,output_grid, expected_grid)

input_grid = np.array([[0, 3, 0, 3, 0],
                       [3, 0, 3, 0, 3],
                       [0, 3, 0, 3, 0],
                       [3, 0, 3, 0, 3],
                       [0, 3, 0, 3, 0]])
output_grid = np.array([[0, 8, 0, 8, 0],
                        [8, 0, 8, 0, 8],
                        [9, 9, 9, 9, 9],
                        [9, 0, 9, 0, 9],
                        [0, 9, 0, 9, 0]])  # current code
expected_grid = np.array([[0, 8, 0, 8, 0],
                          [8, 0, 8, 0, 8],
                          [0, 9, 0, 9, 0],
                          [9, 0, 9, 0, 9],
                          [0, 9, 0, 9, 0]])
analyze_grid(input_grid,output_grid, expected_grid)