import numpy as np

def grid_metrics(grid):
    """Calculates and returns metrics for a given grid."""
    unique_colors = np.unique(grid)
    row_lengths = [len(row) for row in grid]
    color_counts = {color: np.sum(grid == color) for color in unique_colors}
    return {
        "shape": grid.shape,
        "unique_colors": unique_colors.tolist(),  # Convert to list for YAML compatibility
        "row_lengths": row_lengths,
        "color_counts": color_counts,
    }

def analyze_all_examples(examples):
    results = []
    for i, (input_grid, expected_output_grid) in enumerate(examples):
        input_metrics = grid_metrics(input_grid)
        output_metrics = grid_metrics(expected_output_grid)
        results.append({
            "example": i + 1,
            "input": input_metrics,
            "output": output_metrics,
        })
    return results

examples = [
    (
        np.array([[0, 0, 0], [1, 2, 1], [0, 0, 0]]),  # Example 1 Input
        np.array([[0, 0, 0, 0, 0, 0], [1, 2, 1, 1, 2, 1], [0, 0, 0, 0, 0, 0]]),  # Example 1 Expected Output
    ),
      (
        np.array([[0, 0, 0, 0], [1, 2, 1, 2], [0, 0, 0, 0]]),  # Example 2 Input
        np.array([[0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 1, 2, 1, 2, 1, 2], [0, 0, 0, 0, 0, 0, 0, 0]]),  # Example 2 Expected Output
    ),
     (
        np.array([[0, 0, 0, 0, 0], [1, 2, 1, 2, 1], [0, 0, 0, 0, 0]]),  # Example 3 Input
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 2, 1, 2, 1, 1, 2, 1, 2, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),  # Example 3 Expected Output
    )
]

analysis_results = analyze_all_examples(examples)

# Print in a somewhat YAML-like format (proper YAML requires an external library)
for result in analysis_results:
    print(f"- example: {result['example']}")
    print("  input:")
    print(f"    shape: {result['input']['shape']}")
    print(f"    unique_colors: {result['input']['unique_colors']}")
    print(f"    row_lengths: {result['input']['row_lengths']}")
    print(f"    color_counts: {result['input']['color_counts']}")
    print("  output:")
    print(f"    shape: {result['output']['shape']}")
    print(f"    unique_colors: {result['output']['unique_colors']}")
    print(f"    row_lengths: {result['output']['row_lengths']}")
    print(f"    color_counts: {result['output']['color_counts']}")