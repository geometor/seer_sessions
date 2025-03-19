def analyze_grid(grid):
    rows, cols = grid.shape
    gray_pixels = 0
    contiguous_gray_runs = []
    max_contiguous = 0
    for r in range(rows):
        current_run = 0
        for c in range(cols):
            if grid[r,c] == 5:
                gray_pixels += 1
                current_run += 1
            else:
                if current_run > 0:
                    contiguous_gray_runs.append(current_run)
                    max_contiguous = max(max_contiguous, current_run)
                    current_run = 0
        if current_run > 0: #end of row, still in a run
            contiguous_gray_runs.append(current_run)
            max_contiguous = max(max_contiguous, current_run)
            current_run = 0

    return {
        "rows": rows,
        "cols": cols,
        "gray_pixels": gray_pixels,
        "contiguous_gray_runs": contiguous_gray_runs,
        "max_contiguous": max_contiguous
    }

import numpy as np
# Example usage (replace with actual grids from the task):
input_grid1 = np.array([[0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0], [0, 0, 0, 0, 0, 0]])
output_grid1 = np.array([[0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0], [0, 0, 0, 0, 0, 0]])
input_grid2 = np.array([[0, 0, 5, 0, 0, 0], [0, 5, 5, 5, 0, 0], [0, 0, 0, 0, 5, 0]])
output_grid2 = np.array([[0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0], [0, 0, 0, 0, 0, 0]])
input_grid3 = np.array([[5, 0, 0, 5, 5], [0, 5, 0, 0, 0], [0, 5, 5, 0, 5]])
output_grid3 = np.array([[0, 0, 0, 5, 5], [0, 0, 0, 0, 0], [0, 5, 5, 0, 0]])

print("Example 1 Input:", analyze_grid(input_grid1))
print("Example 1 Output:", analyze_grid(output_grid1))
print("Example 2 Input:", analyze_grid(input_grid2))
print("Example 2 Output:", analyze_grid(output_grid2))
print("Example 3 Input:", analyze_grid(input_grid3))
print("Example 3 Output:", analyze_grid(output_grid3))

