import numpy as np

def describe_grid(grid, grid_name):
    """Provides a basic description of a grid."""
    height, width = grid.shape
    unique_colors = np.unique(grid)
    print(f"Grid: {grid_name}")
    print(f"  Dimensions: {height}x{width}")
    print(f"  Unique Colors: {', '.join(map(str, unique_colors))}")
    print(f"{grid_name}:\n", grid)
#Provided examples:
train_ex_in_0=np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
train_ex_out_0=np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])
train_ex_in_1=np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8]])
train_ex_out_1=np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
train_ex_in_2=np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])
train_ex_out_2=np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
train_ex_in_3=np.array([[5, 5, 8, 8, 5, 5], [5, 5, 8, 8, 5, 5]])
train_ex_out_3=np.array([[5, 5, 5, 5, 8, 8, 8, 8, 5, 5, 5, 5], [5, 5, 5, 5, 8, 8, 8, 8, 5, 5, 5, 5], [5, 5, 5, 5, 8, 8, 8, 8, 5, 5, 5, 5], [5, 5, 5, 5, 8, 8, 8, 8, 5, 5, 5, 5]])
train_ex_in_4=np.array([[2, 2, 2, 2], [2, 6, 6, 2], [2, 2, 2, 2]])
train_ex_out_4=np.array([[2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 6, 6, 6, 6, 2, 2], [2, 2, 6, 6, 6, 6, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2]])
#now describe them
describe_grid(train_ex_in_0, "train_ex_in_0")
describe_grid(train_ex_out_0, "train_ex_out_0")
describe_grid(train_ex_in_1, "train_ex_in_1")
describe_grid(train_ex_out_1, "train_ex_out_1")
describe_grid(train_ex_in_2, "train_ex_in_2")
describe_grid(train_ex_out_2, "train_ex_out_2")
describe_grid(train_ex_in_3, "train_ex_in_3")
describe_grid(train_ex_out_3, "train_ex_out_3")
describe_grid(train_ex_in_4, "train_ex_in_4")
describe_grid(train_ex_out_4, "train_ex_out_4")