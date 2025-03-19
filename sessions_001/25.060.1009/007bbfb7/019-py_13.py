def compare_grids(input_grid, output_grid):
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape

    if output_rows != input_rows * 3 or output_cols != input_cols * 3:
        return "Grid size mismatch"

    color_mapping = {}  # input color -> output block color consistency

    for i in range(input_rows):
        for j in range(input_cols):
            input_color = input_grid[i, j]
            output_block_colors = output_grid[i*3:(i+1)*3, j*3:(j+1)*3]
            
            # Check if the output block is uniform in color
            if not np.all(output_block_colors == input_color):
                if input_color not in color_mapping:
                  color_mapping[input_color] = False
            else:
                if input_color not in color_mapping:
                  color_mapping[input_color] = True
    return color_mapping