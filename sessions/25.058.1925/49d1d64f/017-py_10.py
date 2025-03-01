import numpy as np

def analyze_example(input_grid, output_grid):
    input_shape = input_grid.shape
    output_shape = output_grid.shape
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    padding_color = list(set(output_colors) - set(input_colors))
    if not padding_color:
        padding_color = [output_grid[0,0]] #if no difference, assume first pixel

    print(f"  Input shape: {input_shape}")
    print(f"  Output shape: {output_shape}")
    print(f"  Input colors: {input_colors}")
    print(f"  Output colors: {output_colors}")
    print(f"  Padding color: {padding_color[0]}")
    print("---")

example_grids = [
    (np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]), np.array([[0, 0, 0, 0, 0], [0, 5, 5, 5, 0], [0, 5, 5, 5, 0], [0, 5, 5, 5, 0], [0, 0, 0, 0, 0]])),
    (np.array([[1, 1], [1, 1]]), np.array([[1, 1, 0], [1, 1, 0], [0, 0, 0]])),
    (np.array([[8]]), np.array([[8, 0], [0, 0]])),
    (np.array([[7, 7, 7, 7], [7, 7, 7, 7]]), np.array([[7, 7, 7, 7, 0], [7, 7, 7, 7, 0], [0, 0, 0, 0, 0]])),
    (np.array([[4, 4, 4], [4, 4, 4], [4, 4, 4]]), np.array([[4, 4, 4, 0], [4, 4, 4, 0], [4, 4, 4, 0], [0,0,0,0]]))
]

for i, (input_grid, output_grid) in enumerate(example_grids):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
