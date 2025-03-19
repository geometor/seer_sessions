def get_grid_dimensions_and_colors(grid):
    """Returns dimensions (height, width) and a set of unique colors in a grid."""
    dimensions = grid.shape
    unique_colors = set(np.unique(grid).tolist())
    return dimensions, unique_colors

task_data = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[2, 2, 2]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[2, 2]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[2]]
        }
    ]
}

results = []
for example in task_data["train"]:
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])
    predicted_output = transform(input_grid)
    
    input_dims, input_colors = get_grid_dimensions_and_colors(input_grid)
    output_dims, output_colors = get_grid_dimensions_and_colors(output_grid)
    predicted_dims, predicted_colors = get_grid_dimensions_and_colors(predicted_output)

    results.append({
        "input_dims": input_dims,
        "input_colors": input_colors,
        "output_dims": output_dims,
        "output_colors": output_colors,
        "predicted_dims": predicted_dims,
        "predicted_colors": predicted_colors,
        "correct": np.array_equal(output_grid, predicted_output)
    })

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input:  Dimensions - {result['input_dims']}, Colors - {result['input_colors']}")
    print(f"  Output: Dimensions - {result['output_dims']}, Colors - {result['output_colors']}")
    print(f"  Predicted: Dimensions - {result['predicted_dims']}, Colors - {result['predicted_colors']}")
    print(f"  Correct: {result['correct']}")