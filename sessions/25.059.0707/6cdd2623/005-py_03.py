import numpy as np

def analyze_grid(grid, description):
    """Analyzes a grid for green pixel locations and counts."""
    green_pixels = []
    num_rows, num_cols = grid.shape
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r, c] == 3:
                green_pixels.append((r, c))
    print(f"Analysis of {description}:")
    print(f"  Green Pixels: {green_pixels}")
    print(f"  Number of Green Pixels: {len(green_pixels)}")


# Example Grids (assuming these are defined elsewhere, I'll put placeholders)
example_grids = {
   "train_0_in":  np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]]),

    "train_0_out": np.array([[0, 0, 0, 0, 3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 3, 0, 0, 0, 0],
                             [3, 3, 3, 3, 3, 3, 3, 3, 3],
                             [0, 0, 0, 0, 3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 3, 0, 0, 0, 0]]),

    "train_1_in": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 3, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]),

    "train_1_out":  np.array([[0, 0, 0, 0, 0, 3, 0, 0],
                             [3, 3, 3, 3, 3, 3, 3, 3],
                             [0, 0, 0, 0, 0, 3, 0, 0],
                             [0, 0, 0, 0, 0, 3, 0, 0],
                             [0, 0, 0, 0, 0, 3, 0, 0]]),

    "train_2_in": np.array([[0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 3, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]]),
    "train_2_out": np.array([[0, 0, 0, 3, 0, 0],
                            [3, 3, 3, 3, 3, 3],
                            [0, 0, 0, 3, 0, 0],
                            [0, 0, 0, 3, 0, 0],
                            [0, 0, 0, 3, 0, 0],
                            [0, 0, 0, 3, 0, 0]]),
    "train_3_in": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 3, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    "train_3_out": np.array([[0, 0, 0, 0, 3, 0, 0, 0, 0],
       [0, 0, 0, 0, 3, 0, 0, 0, 0],
       [0, 0, 0, 0, 3, 0, 0, 0, 0],
       [0, 0, 0, 0, 3, 0, 0, 0, 0],
       [3, 3, 3, 3, 3, 3, 3, 3, 3],
       [0, 0, 0, 0, 3, 0, 0, 0, 0]])
}


for key, grid in example_grids.items():
    analyze_grid(grid, key)