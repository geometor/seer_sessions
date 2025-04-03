# tool_code
import numpy as np

# Representing inputs/outputs as List[List[int]] based on analysis
train_inputs = [
    [[0, 0, 3, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 8, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0]],
    [[0, 0, 0, 6, 0, 0, 6, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 6, 0, 0, 0, 0]]
]
train_outputs = [
    [[0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0]]
]

print("Input Analysis (Assuming 2D Grid):")
for i, grid in enumerate(train_inputs):
    arr = np.array(grid)
    height, width = arr.shape
    unique_colors = np.unique(arr)
    non_white_colors = unique_colors[unique_colors != 0]
    non_white_color = non_white_colors[0] if len(non_white_colors) > 0 else None
    print(f"Example {i+1}: Shape=({height}x{width}), Unique Colors={unique_colors.tolist()}, Non-White Color={non_white_color}")

print("\nOutput Analysis (Assuming 2D Grid):")
for i, grid in enumerate(train_outputs):
    arr = np.array(grid)
    height, width = arr.shape
    unique_colors = np.unique(arr)
    non_white_colors = unique_colors[unique_colors != 0]
    non_white_color = non_white_colors[0] if len(non_white_colors) > 0 else None
    print(f"Example {i+1}: Shape=({height}x{width}), Unique Colors={unique_colors.tolist()}, Non-White Color={non_white_color}")
