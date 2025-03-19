import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_dims = input_grid.shape
    output_dims = output_grid.shape

    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)

    color_counts = {}
    for color in input_colors:
        color_counts[f"input_{color}"] = np.sum(input_grid == color)
    for color in output_colors:
        color_counts[f"output_{color}"] = np.sum(output_grid == color)
        
    print(f"Input Dimensions: {input_dims}")
    print(f"Output Dimensions: {output_dims}")
    print(f"Input Colors: {input_colors}")
    print(f"Output Colors: {output_colors}")    
    print(f"Color Counts: {color_counts}")


example_data = [
    (
        [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 4, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 9, 0, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 4, 5, 0], [0, 9, 6, 0], [0, 0, 0, 0]]
    ),
    (
      [[0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 9, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 6, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
      [[5, 0, 0, 9], [0, 4, 6, 0], [0, 0, 0, 0], [8, 0, 0, 1]]
    ),
    (
      [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 6, 0, 0, 0], [0, 0, 0, 9, 4, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
      [[0, 0, 0, 0], [0, 5, 6, 0], [0, 9, 4, 0], [0, 0, 0, 0]]
    )
]

for i, (input_grid, output_grid) in enumerate(example_data):
    print(f"--- Example {i + 1} ---")
    analyze_example(input_grid, output_grid)