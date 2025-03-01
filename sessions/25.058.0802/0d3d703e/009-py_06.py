import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)

    color_mapping_check = True
    if input_grid.shape == output_grid.shape:
        for i in range(input_height):
            for j in range(input_width):
                in_val = input_grid[i,j]
                out_val = output_grid[i,j]
                if in_val == 2 and out_val != 6:
                    color_mapping_check = False
                if in_val == 3 and out_val != 4:
                    color_mapping_check = False
                if in_val == 8 and out_val != 9:
                    color_mapping_check = False

    results = {
      'input_dimensions': (input_height, input_width),
      'output_dimensions': (output_height, output_width),
      'input_colors': list(input_colors.astype(int)),
      'output_colors': list(output_colors.astype(int)),
      'color_mapping_correct': color_mapping_check,
      'same_dimensions': input_grid.shape == output_grid.shape

    }
    return results
# dummy data for now
examples = [
    ([[2, 3, 8], [2, 3, 8], [2, 3, 8]], [[6, 4, 9], [6, 4, 9], [6, 4, 9]]),
    ([[8, 2, 3], [8, 2, 3], [8, 2, 3]], [[9, 6, 4], [9, 6, 4], [9, 6, 4]]),
    ([[3, 8, 2], [3, 8, 2], [3, 8, 2]], [[4, 9, 6], [4, 9, 6], [4, 9, 6]]),
]

for i, (input_grid, output_grid) in enumerate(examples):
  analysis = analyze_example(input_grid, output_grid)
  print(f"Example {i+1}:")
  print(analysis)
