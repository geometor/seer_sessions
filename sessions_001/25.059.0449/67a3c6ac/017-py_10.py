def compare_grids(grid1, grid2):
    """Compares two grids and returns the percentage of matching pixels."""
    if grid1.shape != grid2.shape:
        return 0  # Incomparable
    matching_pixels = np.sum(grid1 == grid2)
    total_pixels = grid1.size
    return (matching_pixels / total_pixels) * 100 if total_pixels > 0 else 0

# Load all input and output grids from the training data.
train_data_filepaths = task.train_data_filepaths
test_data_filepaths = task.test_data_filepaths

for example_index, (input_fp, output_fp) in enumerate(train_data_filepaths):
    input_grid = task.load_grid(input_fp)
    output_grid = task.load_grid(output_fp)
    transformed_grid = transform(input_grid)
    match_percentage = compare_grids(transformed_grid, output_grid)
    print(f"Train Example {example_index}: Match Percentage = {match_percentage:.2f}%")
    #print(f"input\n{input_grid}\noutput\n{output_grid}\ntransformed\n{transformed_grid}")
