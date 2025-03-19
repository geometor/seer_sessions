def analyze_grid(grid):
    """Analyzes a single grid and returns relevant properties."""
    grid = np.array(grid)
    num_rows, num_cols = grid.shape
    pixel_counts = {}
    for color in range(10):
        pixel_counts[color] = np.sum(grid == color)
    all_zero_columns = []
    for j in range(num_cols):
        if np.all(grid[:, j] == 0):
            all_zero_columns.append(j)
    return {
        "rows": num_rows,
        "cols": num_cols,
        "pixel_counts": pixel_counts,
        "all_zero_columns": all_zero_columns,
    }

def analyze_example(input_grid, output_grid):
    """Analyzes an input-output pair and identifies changes."""
    input_analysis = analyze_grid(input_grid)
    output_analysis = analyze_grid(output_grid)
    changed_pixels = []
    input_grid_np = np.array(input_grid)
    output_grid_np= np.array(output_grid)

    for r in range(input_analysis['rows']):
      for c in range(input_analysis['cols']):
        if input_grid_np[r,c] != output_grid_np[r,c]:
          changed_pixels.append( (r,c,input_grid_np[r,c], output_grid_np[r,c]))
    return {
        "input": input_analysis,
        "output": output_analysis,
        "changed_pixels": changed_pixels,
    }

# Example data (replace with actual data from the task)
train = task["train"]

# Get the example name

example_analyses = []
for i, example in enumerate(train):
    analysis = analyze_example(example['input'], example['output'])
    example_analyses.append(analysis)

print(example_analyses)