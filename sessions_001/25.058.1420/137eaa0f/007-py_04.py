def get_pixel_counts(grid):
    """Counts the number of pixels of each color in the grid."""
    counts = {}
    for color in range(10):  # Colors 0-9
        counts[color] = np.sum(grid == color)
    return counts

def compare_grids(grid1, grid2):
    """Compares two grids and returns a dictionary of differences."""
    if grid1.shape != grid2.shape:
        return "Different shapes"
    diff = grid1 != grid2
    diff_indices = np.where(diff)
    return list(zip(diff_indices[0], diff_indices[1]))

examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 7],
                           [0, 0, 0, 0, 0, 0, 7],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 5, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 6, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 7],
                            [0, 5, 7],
                            [0, 0, 0]])
    },
    {
         "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [4, 4, 4, 4, 4, 4, 4, 4],
                            [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0],
                           [0, 0, 0],
                           [4, 4, 4, 0, 0, 0, 0, 0]])
    },
    {
       "input": np.array([[0, 0, 0, 0, 0, 7, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 4, 4, 4, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 7],
                            [0, 0, 0],
                            [4, 4, 4, 0, 0, 0, 0, 0]])
    },
        {
        "input": np.array([[6, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 7, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 4, 0, 0, 0, 0]]),
        "output": np.array([[6, 0, 7],
                            [0, 0, 0],
                            [4, 0, 0]])
    }
]

results = []
for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid.copy())  # Use a copy to avoid modifying the original
    pixel_counts_input = get_pixel_counts(input_grid)
    pixel_counts_output = get_pixel_counts(expected_output)
    grid_differences = compare_grids(expected_output, predicted_output)

    results.append({
        "example_index": i,
        "input_shape": input_grid.shape,
        "output_shape": expected_output.shape,
        "predicted_output_shape": predicted_output.shape,
        "input_pixel_counts": pixel_counts_input,
        "output_pixel_counts": pixel_counts_output,
        "grid_differences": grid_differences
    })

for result in results:
    print(result)
