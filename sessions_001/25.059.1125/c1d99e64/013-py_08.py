import numpy as np

def report(grid, grid_name):
    """Generates a report on the grid's properties."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    white_lines = []
    for col in range(cols):
        in_segment = False
        start_row = -1
        for row in range(rows):
            if grid[row, col] == 0:
                if not in_segment:
                    in_segment = True
                    start_row = row
            elif in_segment:
                in_segment = False
                white_lines.append((start_row, row - 1, col))
                start_row = -1
        if in_segment:
            white_lines.append((start_row, rows - 1, col))

    max_white_line_length = 0
    if white_lines:
        max_white_line_length = max(end - start + 1 for start, end, _ in white_lines)
    
    print(f"Report for {grid_name}:")
    print(f"  Dimensions: {rows}x{cols}")
    print(f"  Unique Colors: {unique_colors}")
    print(f"  White Lines (start_row, end_row, col): {white_lines}")
    print(f"  Max White Line Length: {max_white_line_length}")
    print("---")

# Example Grids (replace with actual data from the task)
example_grids = {
    "train_0_in": np.array([[6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 0, 0, 6, 6, 6, 6, 6], [6, 6, 0, 0, 6, 6, 6, 0, 6], [6, 6, 0, 0, 6, 6, 6, 0, 6], [6, 6, 6, 6, 6, 6, 6, 0, 6]]),
    "train_0_out": np.array([[6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 1, 1, 6, 6, 6, 6, 6], [6, 6, 1, 1, 6, 6, 6, 0, 6], [6, 6, 1, 1, 6, 6, 6, 0, 6], [6, 6, 6, 6, 6, 6, 6, 0, 6]]),
    "train_1_in": np.array([[7, 7, 7, 7, 7, 7, 7], [7, 0, 0, 0, 7, 7, 7], [7, 0, 0, 0, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7]]),
    "train_1_out": np.array([[7, 7, 7, 7, 7, 7, 7], [7, 1, 1, 1, 7, 7, 7], [7, 1, 1, 1, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7]]),
    "train_2_in": np.array([[6, 6, 6, 6, 6, 6], [6, 6, 0, 6, 6, 6], [6, 6, 0, 6, 6, 6], [6, 6, 6, 6, 6, 6]]),
    "train_2_out": np.array([[6, 6, 6, 6, 6, 6], [6, 6, 2, 6, 6, 6], [6, 6, 2, 6, 6, 6], [6, 6, 6, 6, 6, 6]]),
    "train_3_in": np.array([[0, 6, 6, 6, 6, 6, 6, 6], [0, 6, 6, 0, 0, 6, 6, 6], [0, 6, 6, 0, 0, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6]]),
    "train_3_out": np.array([[4, 6, 6, 6, 6, 6, 6, 6], [4, 6, 6, 0, 0, 6, 6, 6], [4, 6, 6, 0, 0, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6]]),
    "train_4_in": np.array([[5, 5, 5, 0, 0, 5, 5, 5], [5, 5, 5, 0, 0, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5]]),
    "train_4_out": np.array([[5, 5, 5, 0, 0, 5, 5, 5], [5, 5, 5, 0, 0, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5]]),
}

for name, grid in example_grids.items():
    report(grid, name)
