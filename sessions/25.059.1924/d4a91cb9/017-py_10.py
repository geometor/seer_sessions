import numpy as np

def find_pixel(grid, color):
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return (coords[0][0], coords[1][0])
    return None

def analyze_grid(input_grid, output_grid):
    azure_pixel = find_pixel(input_grid, 8)
    red_pixel = find_pixel(input_grid, 2)
    grid_dims = input_grid.shape

    print(f"  Azure Pixel: {azure_pixel}")
    print(f"  Red Pixel: {red_pixel}")
    print(f"  Grid Dimensions: {grid_dims}")

    if azure_pixel and red_pixel:
        row_diff = red_pixel[0] - azure_pixel[0]
        col_diff = red_pixel[1] - azure_pixel[1]
        print(f"  Relative Position: Red is ({row_diff}, {col_diff}) from Azure")

    yellow_pixels = np.where(output_grid == 4)
    if len(yellow_pixels[0]) > 0:
      diff = output_grid - input_grid
      coords = np.where(diff == 4)
      #convert the coordinate arrays into a list of (row, col) pairs
      yellow_connector = list(zip(coords[0],coords[1]))
      print(f"  Yellow Connector: {yellow_connector}")
    else:
        print("  Yellow Connector: None")
    print("---")

task = c79d2a80
train_inputs = [
    np.array([[8, 1, 1], [1, 1, 1], [1, 1, 2]]),
    np.array([[1, 1, 1, 8, 1], [1, 2, 1, 1, 1]]),
    np.array([[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 2, 1], [1, 8, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]),
]
train_outputs = [
    np.array([[8, 1, 1], [4, 1, 1], [4, 1, 2]]),
    np.array([[1, 1, 1, 8, 4], [1, 2, 1, 1, 4]]),
    np.array([[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 2, 4], [1, 8, 1, 1, 1, 1, 4, 4], [1, 1, 1, 1, 1, 1, 1, 1]]),
]

test_input = np.array([[1, 1, 1, 1, 1], [1, 1, 2, 1, 1], [1, 1, 1, 1, 1], [1, 1, 8, 1, 1], [1, 1, 1, 1, 1]])

print(f"Task: {task}")
print("Train Examples:")
for i, (input_grid, output_grid) in enumerate(zip(train_inputs, train_outputs)):
    print(f"Example {i+1}:")
    analyze_grid(input_grid, output_grid)
