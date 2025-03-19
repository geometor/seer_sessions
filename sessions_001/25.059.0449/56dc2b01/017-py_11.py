task_id = '6d0a4119'
training_examples = [
    {
        "input": [
            [0, 0, 0, 0, 0],
            [0, 3, 3, 3, 3],
            [0, 3, 3, 3, 3],
            [2, 2, 2, 2, 2],
            [0, 3, 3, 3, 3],
            [0, 3, 3, 3, 3],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2],
            [0, 3, 3, 3, 3],
            [0, 3, 3, 3, 3],
            [0, 0, 0, 0, 0],
            [8, 8, 8, 8, 8],
            [0, 0, 0, 0, 0],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 3, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 3, 3, 0],
            [0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 3, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 3, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0],
            [3, 3, 3, 3, 0, 0],
            [3, 3, 3, 3, 0, 0],
            [3, 3, 3, 3, 0, 0],
            [2, 2, 2, 0, 0, 0],
            [3, 3, 3, 3, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [2, 2, 2, 0, 0, 0],
            [3, 3, 3, 3, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [8, 8, 8, 8, 8, 8],
        ],
    },
]

def find_object(grid, color):
    """Finds the bounding box of the largest contiguous block of the given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def get_horizontal_line(grid, color, row_index):
    """Extracts a horizontal line of given color and row index."""
    line_cols = np.where(grid[row_index,:] == color)[0]
    if line_cols.size == 0:
        return None

    return (row_index, np.min(line_cols)), (row_index,np.max(line_cols))
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # 1. Preserve the Red Line
    red_line = get_horizontal_line(input_grid, 2, 3)
    if red_line:
      (r_start, c_start), (r_end, c_end) = red_line
      output_grid[r_start, c_start:c_end+1] = 2
      red_line_row = r_start

    # 2. Partially remove and shift the Green Shape
    green_object = find_object(input_grid, 3)
    if green_object:
        (green_min_row, green_min_col), (green_max_row, green_max_col) = green_object
        #Copy only two rows of green, and place them just after the red line
        new_green_start_row = red_line_row + 1
        rows_to_copy = 2
        if new_green_start_row + rows_to_copy <= output_grid.shape[0]:            
            output_grid[new_green_start_row:new_green_start_row + rows_to_copy, green_min_col:green_max_col+1] = input_grid[green_max_row-rows_to_copy+1:green_max_row+1, green_min_col:green_max_col+1]

        #3 Add the azure line
        azure_row = new_green_start_row + rows_to_copy + 3 # add 3 for padding
        if azure_row < output_grid.shape[0]:
          output_grid[azure_row,:] = 8

    return output_grid


for i, example in enumerate(training_examples):
  input_grid = np.array(example["input"])
  expected_output = np.array(example["output"])
  print(f"Example {i+1}:")
  print(code_execution(input_grid, example["output"], expected_output, transform))
