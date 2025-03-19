def get_metrics(input_grid, output_grid):
    """
    Calculates and returns metrics comparing the input and output grids.
    """
    input_red_count = 0
    output_red_count = 0
    input_azure_count = 0
    output_azure_count = 0

    for row in input_grid:
        for pixel in row:
            if pixel == 2:
                input_red_count += 1
            elif pixel == 8:
                input_azure_count += 1

    for row in output_grid:
        for pixel in row:
            if pixel == 2:
                output_red_count += 1
            elif pixel == 8:
                output_azure_count += 1
    
    red_pixels_by_column_input = {}
    red_pixels_by_column_output = {}
    
    
    for row_index, row in enumerate(input_grid):
        for col_index, pixel in enumerate(row):
            if pixel == 2:
                if col_index not in red_pixels_by_column_input:
                    red_pixels_by_column_input[col_index] = 0
                red_pixels_by_column_input[col_index] += 1    
                
    for row_index, row in enumerate(output_grid):
        for col_index, pixel in enumerate(row):
            if pixel == 2:
                if col_index not in red_pixels_by_column_output:
                    red_pixels_by_column_output[col_index] = 0
                red_pixels_by_column_output[col_index] += 1

    return {
        "input_red_count": input_red_count,
        "output_red_count": output_red_count,
        "input_azure_count": input_azure_count,
        "output_azure_count": output_azure_count,
        "red_pixels_by_column_input": red_pixels_by_column_input,
        "red_pixels_by_column_output" : red_pixels_by_column_output
    }

#sample usage - i will use this to test the examples.
# metrics = get_metrics(train_input_0, train_output_0)
# print(metrics)
