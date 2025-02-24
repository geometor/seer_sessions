def get_grid_info(grid):
    height, width = grid.shape
    colors = np.unique(grid).tolist()
    return {
        "height": height,
        "width": width,
        "colors": colors
    }

results = []

for i, example in enumerate(task["train"]):

    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output = transform(input_grid)
    match = np.array_equal(predicted_output, output_grid)

    input_info = get_grid_info(input_grid)
    output_info = get_grid_info(output_grid)

    results.append(
      {
        "example": i,
        "input": input_info,
        "output": output_info,
        "predicted_output_match": match
      }
    )

print(results)