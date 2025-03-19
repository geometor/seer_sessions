import numpy as np

def analyze_grid(grid, grid_name):
    """Analyzes a single grid and returns relevant properties."""
    rows, cols = grid.shape
    center_col = cols // 2
    
    # Find contiguous white segments vertically
    white_segments = []
    in_segment = False
    start_row = -1
    for row in range(rows):
        if grid[row, center_col] == 0:
            if not in_segment:
                in_segment = True
                start_row = row
        elif in_segment:
            in_segment = False
            white_segments.append((start_row, row - 1, row - start_row))
            start_row = -1
    if in_segment:
        white_segments.append((start_row, rows - 1, rows - start_row))
        
    max_segment = max(white_segments, key=lambda x: x[2], default=(-1, -1, 0))
    unique_colors = np.unique(grid)

    print(f"--- {grid_name} ---")
    print(f"Dimensions: {rows}x{cols}")
    print(f"Center Column: {center_col}")
    print(f"White Segments (start_row, end_row, length): {white_segments}")
    print(f"Longest White Segment: {max_segment}")
    print(f"Unique Colors: {unique_colors}")

def compare_grids(input_grid, output_grid, example_name):
    """Compares input and output, printing differences."""
    
    analyze_grid(input_grid, f"{example_name} Input")
    analyze_grid(output_grid, f"{example_name} Output")

    diff = input_grid != output_grid
    if np.any(diff):
        print(f"Differences found in {example_name}:")
        diff_coords = np.where(diff)
        for r, c in zip(diff_coords[0], diff_coords[1]):
            print(f"  Row: {r}, Col: {c}, Input: {input_grid[r, c]}, Output: {output_grid[r, c]}")
    else:
        print(f"No differences found in {example_name}.")


# Example grids from the training set (replace with actual data)
example_grids = {
    "train_0": (
        np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 0, 0, 0, 0, 0, 8, 8],
                  [8, 0, 0, 0, 0, 0, 0, 0, 8],
                  [8, 8, 0, 0, 0, 0, 0, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 2, 2, 2, 2, 2, 8, 8],
                  [8, 2, 2, 2, 2, 2, 2, 2, 8],
                  [8, 8, 2, 2, 2, 2, 2, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8, 8]])
    ),
     "train_1": (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1]])
    ),
    "train_2": (
        np.array([[0, 0, 0, 0, 0, 0, 0],
                  [0, 5, 5, 5, 5, 5, 0],
                  [0, 5, 5, 5, 5, 5, 0],
                  [0, 5, 5, 5, 5, 5, 0],
                  [0, 0, 0, 0, 0, 0, 0]]),
        np.array([[3, 3, 3, 3, 3, 3, 3],
                  [3, 5, 5, 5, 5, 5, 3],
                  [3, 5, 5, 5, 5, 5, 3],
                  [3, 5, 5, 5, 5, 5, 3],
                  [3, 3, 3, 3, 3, 3, 3]])
    ),
    "train_3": (
        np.array([[6, 0, 6, 0, 6, 0, 6],
                  [0, 6, 0, 6, 0, 6, 0],
                  [6, 0, 6, 0, 6, 0, 6],
                  [0, 6, 0, 6, 0, 6, 0],
                  [6, 0, 6, 0, 6, 0, 6],
                  [0, 6, 0, 6, 0, 6, 0]]),
        np.array([[6, 1, 6, 1, 6, 1, 6],
                  [1, 6, 1, 6, 1, 6, 1],
                  [6, 1, 6, 1, 6, 1, 6],
                  [1, 6, 1, 6, 1, 6, 1],
                  [6, 1, 6, 1, 6, 1, 6],
                  [1, 6, 1, 6, 1, 6, 1]])
    ),
    "train_4": (
        np.array([[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0]]),
        np.array([[4, 4, 4, 4, 4],
                  [4, 4, 4, 4, 4],
                  [4, 4, 4, 4, 4],
                  [4, 4, 4, 4, 4],
                  [4, 4, 4, 4, 4],
                  [4, 4, 4, 4, 4]])
    ),

}

for example_name, (input_grid, output_grid) in example_grids.items():
    compare_grids(input_grid, output_grid, example_name)