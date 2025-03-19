def code_execution(input_grid, output_grid):
    input_azure_regions = find_azure_regions(np.array(input_grid))
    output_azure_regions = find_azure_regions(np.array(output_grid))
    # check for blue in output
    output_blue_regions = []
    rows, cols = np.array(output_grid).shape
    for r in range(rows):
        start_col = None
        for c in range(cols):
            if output_grid[r][c] == 1: # blue
                if start_col is None:
                    start_col = c
            elif start_col is not None:
                length = c - start_col
                output_blue_regions.append({
                    'start_row': r,
                    'start_col': start_col,
                    'end_col': c - 1,
                    'length': length
                })
                start_col = None
        if start_col is not None:
            length = cols - start_col
            output_blue_regions.append({
              'start_row': r,
              'start_col': start_col,
              'end_col': cols -1,
              'length': length
            })

    print(f"Input Azure Regions: {input_azure_regions}")
    print(f"Output Azure Regions: {output_azure_regions}")
    print(f"Output Blue Regions: {output_blue_regions}")

# Example usage with the first training pair:
task_data = _get_task_data('3618c87e')

for i, (train_input, train_output) in enumerate(task_data["train"]):
    print(f"== Train Example {i} ==")
    code_execution(train_input['grid'], train_output['grid'])
