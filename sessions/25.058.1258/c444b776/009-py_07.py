import numpy as np

def calculate_grid_stats(grid, grid_name):
    """Calculates and returns statistics for a given grid."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    num_unique_colors = len(unique_colors)
    color_counts = {color: np.sum(grid == color) for color in unique_colors}

    stats = {
        f"{grid_name}_rows": rows,
        f"{grid_name}_cols": cols,
        f"{grid_name}_unique_colors": num_unique_colors,
        f"{grid_name}_color_counts": color_counts,
    }
    return stats

def report_grid_difference(grid1, grid2, grid1name="input", grid2name="output"):
    if grid1.shape != grid2.shape:
        return "Different Shape"
    else:
        return np.array_equal(grid1, grid2)
# Example grids (replace with actual data from ARC tasks)
# example 1
example1_input = np.array([[8, 0, 8, 8, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 8, 8, 8, 8, 8], [8, 0, 8, 8, 8, 8, 8, 8, 8], [8, 0, 8, 8, 8, 8, 8, 8, 8], [8, 0, 8, 8, 8, 8, 8, 8, 8], [8, 0, 8, 8, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 8, 8, 8, 8, 8]])
example1_output = np.array([[8, 8, 8, 8, 8, 8, 8, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 0, 8], [8, 8, 8, 8, 8, 8, 8, 0, 8], [8, 8, 8, 8, 8, 8, 8, 0, 8], [8, 8, 8, 8, 8, 8, 8, 0, 8], [8, 8, 8, 8, 8, 8, 8, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 0, 8]])
example1_result = transform(example1_input)
# example 2
example2_input = np.array([[8, 0, 8, 8, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 8, 8, 8, 8, 8], [8, 0, 8, 8, 8, 4, 8, 8, 8], [8, 0, 8, 8, 8, 8, 8, 8, 8], [8, 0, 8, 8, 8, 8, 8, 8, 8], [8, 0, 8, 8, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 8, 8, 8, 8, 8]])
example2_output = np.array([[8, 8, 8, 8, 8, 8, 8, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 0, 8], [8, 8, 8, 4, 8, 8, 8, 0, 8], [8, 8, 8, 8, 8, 8, 8, 0, 8], [8, 8, 8, 8, 8, 8, 8, 0, 8], [8, 8, 8, 8, 8, 8, 8, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 0, 8]])
example2_result = transform(example2_input)

# example 3
example3_input = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 4, 4, 4, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]])
example3_output = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 4, 4, 4, 8, 8, 8]])
example3_result = transform(example3_input)

# example 4
example4_input = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [4, 4, 4, 4, 4, 4, 4, 4, 4], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]])
example4_output = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8], [4, 4, 4, 4, 4, 4, 4, 4, 4]])
example4_result = transform(example4_input)

examples = [
    (example1_input, example1_output, example1_result),
    (example2_input, example2_output, example2_result),
    (example3_input, example3_output, example3_result),
    (example4_input, example4_output, example4_result)
]

for i, (input_grid, output_grid, result_grid) in enumerate(examples):
  print(f"Example {i+1}:")
  print(f"  Correct: {report_grid_difference(output_grid, result_grid, 'output', 'result')}")
  input_stats = calculate_grid_stats(input_grid, "input")
  output_stats = calculate_grid_stats(output_grid, "output")

  for key in input_stats:
    print(f"  {key}: {input_stats[key]}")
  for key in output_stats:
    print(f"  {key}: {output_stats[key]}")
