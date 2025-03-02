import numpy as np

def analyze_example(input_grid, output_grid, code_output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    code_output_grid = np.array(code_output_grid)

    input_dims = input_grid.shape
    output_dims = output_grid.shape

    input_colors, input_counts = np.unique(input_grid, return_counts=True)
    input_color_counts = dict(zip(input_colors, input_counts))

    output_colors = np.unique(output_grid)

    code_matches = np.array_equal(output_grid, code_output_grid)
    print(f"  Input Dimensions: {input_dims}")
    print(f"  Output Dimensions: {output_dims}")
    print(f"  Input Colors & Counts: {input_color_counts}")
    print(f"  Output Colors: {output_colors}")
    print(f"  Code Matches Expected: {code_matches}")

# provided examples:
train_ex = [
    [[[3, 3, 3], [3, 3, 3], [3, 3, 3]], [[3]]],
    [[[3, 0, 3], [0, 3, 0], [3, 0, 3]], [[0]]],
    [[[1, 1, 1], [8, 8, 8], [8, 8, 8]], [[1]]],
    [[[5, 5, 5], [5, 5, 5]], [[5]]],
    [[[5], [5], [5], [5], [5]], [[5]]]
]

previous_code_outputs = [
  [[3]],
  [[0]],
  [[1]],
  [[5]],
  [[5]]
]

for i, (input_grid, output_grid) in enumerate(train_ex):
    code_output_grid = previous_code_outputs[i]
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid, code_output_grid)
    print("-" * 20)