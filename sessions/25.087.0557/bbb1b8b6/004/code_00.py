# Helper to get unique non-zero colors
import numpy as np
input_grid_np = np.array(examples["ex5"]["input"], dtype=int)
right_subgrid = input_grid_np[:, 5:9]
unique_colors_r = set(np.unique(right_subgrid[right_subgrid != 0]))
print(unique_colors_r)

input_grid_np = np.array(examples["ex6"]["input"], dtype=int)
right_subgrid = input_grid_np[:, 5:9]
unique_colors_r = set(np.unique(right_subgrid[right_subgrid != 0]))
print(unique_colors_r)

input_grid_np = np.array(examples["ex4"]["input"], dtype=int)
right_subgrid = input_grid_np[:, 5:9]
unique_colors_r = set(np.unique(right_subgrid[right_subgrid != 0]))
print(unique_colors_r)

input_grid_np = np.array(examples["ex7"]["input"], dtype=int)
right_subgrid = input_grid_np[:, 5:9]
unique_colors_r = set(np.unique(right_subgrid[right_subgrid != 0]))
print(unique_colors_r)

input_grid_np = np.array(examples["ex3"]["input"], dtype=int)
right_subgrid = input_grid_np[:, 5:9]
unique_colors_r = set(np.unique(right_subgrid[right_subgrid != 0]))
print(unique_colors_r) # Contains only Green (3)
# Rule needs adjustment: In Ex3 (l==r), R contains only Green(3), but output is overlay(R, L), not L.
