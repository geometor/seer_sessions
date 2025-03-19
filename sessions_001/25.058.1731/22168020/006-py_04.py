def get_green_rows_and_cols(grid):
    """
    Finds the rows and columns that contain green pixels
    """
    green_rows = set()
    green_cols = set()
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == 3:
                green_rows.add(row_idx)
                green_cols.add(col_idx)
    return sorted(list(green_rows)), sorted(list(green_cols))

# Example usage and result collection
results = []
for i, example in enumerate(task.train):
    input_grid = example["input"]
    output_grid = example["output"]

    input_green_rows, input_green_cols = get_green_rows_and_cols(np.array(input_grid))
    output_green_rows, output_green_cols = get_green_rows_and_cols(np.array(output_grid))

    results.append({
        "example": i + 1,
        "input_green_rows": input_green_rows,
        "input_green_cols": input_green_cols,
        "output_green_rows": output_green_rows,
        "output_green_cols": output_green_cols,
    })

for r in results:
    print(r)