import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_azure_coords = np.argwhere(input_grid == 8)
    input_red_coords = np.argwhere(input_grid == 2)
    output_azure_coords = np.argwhere(output_grid == 8)

    print("Input Grid Shape:", input_grid.shape)
    print("Output Grid Shape:", output_grid.shape)
    print("Input Azure Pixel Coordinates:", input_azure_coords)
    print("Input Red Pixel Coordinates:", input_red_coords)
    print("Output Azure Pixel Coordinates:", output_azure_coords)
    print("-" * 20)

# Example data (replace with actual data from the task)
examples = [
 ([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
],
[
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]),   
([
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 2, 0, 0, 0],
],
[
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]),
([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 2],
    [0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 0],
],
[
    [8, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 8],
]),
]

for input_grid, output_grid in examples:
    analyze_example(input_grid, output_grid)