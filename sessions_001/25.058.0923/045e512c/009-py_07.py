import numpy as np

def describe_grid(grid, title):
    print(f"\n{title}:")
    print(f"  Shape: {grid.shape}")
    print(f"  Unique values: {np.unique(grid)}")
    blue_pixels = np.argwhere(grid == 1)
    red_pixels = np.argwhere(grid == 2)
    yellow_pixels = np.argwhere(grid == 4)    
    print(f"  Blue pixel count: {len(blue_pixels)}")
    print(f"    Locations: {blue_pixels}")    
    print(f"  Red pixel count: {len(red_pixels)}")
    print(f"    Locations: {red_pixels}")    
    print(f"  Yellow pixel count: {len(yellow_pixels)}")
    print(f"    Locations: {yellow_pixels}")

def compare_grids(grid1, grid2):
    print("\nComparison:")
    if grid1.shape != grid2.shape:
        print(f"  Shapes differ: {grid1.shape} vs {grid2.shape}")
        return
    diff = grid1 != grid2
    num_diff = np.sum(diff)
    print(f"  Number of differing pixels: {num_diff}")
    if num_diff > 0:
      diff_indices = np.argwhere(diff)
      print(f" First 5 differing pixels {diff_indices[:5]}")
      print(f"  Values at first differing pixel:")
      print(f"    Grid 1: {grid1[diff_indices[0][0], diff_indices[0][1]]}")
      print(f"    Grid 2: {grid2[diff_indices[0][0], diff_indices[0][1]]}")
    else:
      print(f" Grids are identical")

train_input_0 = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,2,1,4,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
train_output_0 = np.array([[0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,4,4,4,4,4,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,1,4,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,4,4,4,4,4,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0]])

train_input_1 = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,4,0,0,0,0,0,0],
                          [0,0,0,0,0,0,2,1,4,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

train_output_1 = np.array([[0,0,0,0,0,0,2,2,2,2,2,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0],
                           [0,0,0,0,0,0,4,4,4,4,4,0,0,0,0],
                           [0,0,0,0,0,0,2,1,4,0,0,0,0,0,0],
                           [0,0,0,0,0,0,4,4,4,4,4,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0],
                           [0,0,0,0,0,0,2,2,2,2,2,0,0,0,0]])

train_input_2 = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,4,4,4,0,0,0,0],
                          [0,0,0,0,0,2,1,4,0,0,0,0,0],
                          [0,0,0,0,0,0,2,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0]])
train_output_2 = np.array([[0,0,0,0,0,2,2,2,2,2,0,0,0],
                           [0,0,0,0,0,2,2,2,2,2,0,0,0],
                           [0,0,0,0,0,4,4,4,4,4,0,0,0],
                           [0,0,0,0,0,2,1,4,0,0,0,0,0],
                           [0,0,0,0,0,4,4,4,4,4,0,0,0],
                           [0,0,0,0,0,2,2,2,2,2,0,0,0],
                           [0,0,0,0,0,2,2,2,2,2,0,0,0]])

from previous_code import transform

describe_grid(train_input_0, "Train Input 0")
describe_grid(train_output_0, "Train Output 0")
output_0_predicted = transform(train_input_0)
describe_grid(output_0_predicted, "Predicted Output 0")
compare_grids(train_output_0, output_0_predicted)

describe_grid(train_input_1, "Train Input 1")
describe_grid(train_output_1, "Train Output 1")
output_1_predicted = transform(train_input_1)
describe_grid(output_1_predicted, "Predicted Output 1")
compare_grids(train_output_1, output_1_predicted)

describe_grid(train_input_2, "Train Input 2")
describe_grid(train_output_2, "Train Output 2")
output_2_predicted = transform(train_input_2)
describe_grid(output_2_predicted, "Predicted Output 2")
compare_grids(train_output_2, output_2_predicted)