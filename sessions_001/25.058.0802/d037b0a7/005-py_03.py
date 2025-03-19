import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)
    magenta_present_input = 6 in input_colors
    magenta_present_output = 6 in output_colors

    print(f"Input Colors: {input_colors}")
    print(f"Output Colors: {output_colors}")
    print(f"Magenta in Input: {magenta_present_input}")
    print(f"Magenta in Output: {magenta_present_output}")

    if magenta_present_input:
      magenta_indices_input = np.where(input_grid == 6)
      print(f"Indices of Magenta in Input: {list(zip(magenta_indices_input[0], magenta_indices_input[1]))}")
      magenta_indices_output = np.where(output_grid == 6)
      print(f"Indices of Magenta in Output: {list(zip(magenta_indices_output[0], magenta_indices_output[1]))}")

    # Analyze differences
    diff = input_grid != output_grid
    changed_indices = np.where(diff)
    print(f"Indices of Changed Pixels: {list(zip(changed_indices[0], changed_indices[1]))}")
    for r, c in zip(changed_indices[0], changed_indices[1]):
      print(f"  Pixel ({r}, {c}): Input={input_grid[r, c]}, Output={output_grid[r, c]}")

# Example usage (replace with actual input/output pairs)
examples = [
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 2, 2, 2]], [[2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0, 0, 6, 6, 6], [0, 0, 0, 0, 0, 0, 6, 6, 6, 6], [0, 0, 0, 0, 0, 6, 6, 6, 6, 6], [0, 0, 0, 0, 6, 6, 6, 6, 6, 6], [0, 0, 0, 6, 6, 6, 6, 6, 6, 6], [0, 0, 6, 6, 6, 6, 6, 6, 6, 6], [0, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]], [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 2, 2, 2]], [[2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 6], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2]])
]

for i, (input_grid, output_grid) in enumerate(examples):
  print(f"--- Example {i+1} ---")
  analyze_example(input_grid, output_grid)