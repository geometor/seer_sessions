def describe_grid(grid):
    blue_row = find_horizontal_stripe(grid, 1)
    magenta_cols = find_vertical_stripe(grid, 6)
    print(f"  Blue Horizontal Stripe Row: {blue_row}")
    print(f"  Magenta Vertical Stripe Columns: {magenta_cols}")

for i in range(len(task_train_input_output_list)):

    input_grid = task_train_input_output_list[i][0]
    output_grid = task_train_input_output_list[i][1]

    print(f"Example {i}:")
    print("Input:")
    describe_grid(input_grid)
    print("Output:")
    describe_grid(output_grid)
