import numpy as np

def analyze_grid(grid, label):
    print(f"--- Analysis of {label} ---")
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print("Color Counts:", color_counts)
    # Further analysis (object detection, adjacency, etc.) could be added here.

# Example Grids (replace with actual data loading)
train_in_1 = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0],
    [0, 0, 3, 3, 0, 0],
    [0, 0, 0, 0, 3, 0],
    [3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

train_out_1 = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0],
    [0, 0, 3, 3, 0, 0],
    [0, 0, 0, 0, 4, 0],
    [4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])

train_in_2 = np.array([
    [0, 0, 0, 0, 0],
    [0, 3, 0, 3, 0],
    [0, 0, 0, 0, 0],
    [0, 3, 0, 3, 0],
    [0, 0, 0, 0, 0]
])

train_out_2 = np.array([
    [0, 0, 0, 0, 0],
    [0, 4, 0, 4, 0],
    [0, 0, 0, 0, 0],
    [0, 3, 0, 3, 0],
    [0, 0, 0, 0, 0]
])

train_in_3 = np.array([
    [0, 3, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 3],
    [0, 0, 0, 0, 0, 0]
])

train_out_3 = np.array([
    [0, 4, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 4],
    [0, 0, 0, 0, 0, 0]
])
analyze_grid(train_in_1, "Train Input 1")
analyze_grid(train_out_1, "Train Output 1")
analyze_grid(train_in_2, "Train Input 2")
analyze_grid(train_out_2, "Train Output 2")
analyze_grid(train_in_3, "Train Input 3")
analyze_grid(train_out_3, "Train Output 3")
