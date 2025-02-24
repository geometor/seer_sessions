def get_grid_metrics(grid):
    """Calculates and returns metrics for a given grid."""
    dimensions = grid.shape
    unique_colors = np.unique(grid)
    return {
        "dimensions": dimensions,
        "unique_colors": unique_colors.tolist(),
    }

def analyze_example(input_grid, output_grid):
    """Analyzes an input-output pair and returns relevant metrics."""
    input_metrics = get_grid_metrics(input_grid)
    output_metrics = get_grid_metrics(output_grid)

    pixel_changes = {}
    for color in input_metrics["unique_colors"]:
        if color in output_metrics["unique_colors"]:
            pixel_changes[color] = "present in both"
        else:
           pixel_changes[color] = "removed"

    for color in output_metrics["unique_colors"]:
        if color not in input_metrics["unique_colors"]:
            pixel_changes[color] = "added"


    return {
        "input": input_metrics,
        "output": output_metrics,
        "pixel_changes": pixel_changes,
        "size_change": input_metrics["dimensions"] == output_metrics["dimensions"]
    }

# Assuming 'task' contains the training examples
for i, example in enumerate(task["train"]):
    analysis = analyze_example(np.array(example["input"]), np.array(example["output"]))
    print(f"--- Example {i+1} ---")
    print(f"Input Metrics: {analysis['input']}")
    print(f"Output Metrics: {analysis['output']}")
    print(f"Pixel Changes: {analysis['pixel_changes']}")
    print(f"Size Change: {analysis['size_change']}")
