import numpy as np

def analyze_example(input_grid, output_grid, example_name):
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape
    height_factor = output_height // input_height if input_height !=0 else 0
    width_factor = output_width // input_width if input_width != 0 else 0

    print(f"Example: {example_name}")
    print(f"Input shape: {input_grid.shape}, Output shape: {output_grid.shape}")
    print(f"Replication factor (height): {height_factor}, (width): {width_factor}")
    unique_colors_input = np.unique(input_grid)
    unique_colors_output = np.unique(output_grid)    
    print(f"Unique colors in input: {unique_colors_input}")
    print(f"Unique colors in output: {unique_colors_output}")

    # Calculate padding amounts
    pad_top = 0
    pad_bottom = 0
    pad_left = 0
    pad_right = 0

    # Find contiguous blocks of the input color
    for color in unique_colors_input:
      if color in unique_colors_output:
        # Find the first occurrence of the color in the output grid
        rows, cols = np.where(output_grid == color)
        if len(rows) > 0:
            first_row, first_col = rows[0], cols[0]
            last_row, last_col = rows[-1], cols[-1]

            pad_top = first_row
            pad_left = first_col
            pad_bottom = output_height - 1 - last_row
            pad_right = output_width - 1- last_col

    print(f"Padding - Top: {pad_top}, Bottom: {pad_bottom}, Left: {pad_left}, Right: {pad_right}")
    print("-" * 40)


#train/0eaf60c3
input_grid1 = np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]])
output_grid1 = np.array([[0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 5, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
analyze_example(input_grid1, output_grid1, "train/0eaf60c3")
#train/1e0a9b12
input_grid2 = np.array([[8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8,], [8, 8, 8, 8, 8, 8,]])
output_grid2 = np.array([[8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
analyze_example(input_grid2, output_grid2, "train/1e0a9b12")
# train/32e75207
input_grid3 = np.array([[6, 6, 6], [6, 6, 6], [6, 6, 6]])
output_grid3 = np.array([[0, 0, 0, 6, 6, 6, 0, 0, 0], [0, 0, 0, 6, 6, 6, 0, 0, 0], [0, 0, 0, 6, 6, 6, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 6, 6, 0, 0, 0], [0, 0, 0, 6, 6, 6, 0, 0, 0], [0, 0, 0, 6, 6, 6, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
analyze_example(input_grid3, output_grid3, "train/32e75207")
# train/42a50994
input_grid4 = np.array([[7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7]])
output_grid4 = np.array([[7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
analyze_example(input_grid4, output_grid4, "train/42a50994")
# train/543a7ed5
input_grid5 = np.array([[2, 2, 2], [2, 2, 2]])
output_grid5 = np.array([[2, 2, 2, 0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 0, 0, 0, 0]])
analyze_example(input_grid5, output_grid5, "train/543a7ed5")