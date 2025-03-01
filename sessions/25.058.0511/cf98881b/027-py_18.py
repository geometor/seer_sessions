def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a list of discrepancies.
    """
    grid1 = np.array(grid1)
    grid2 = np.array(grid2)

    if grid1.shape != grid2.shape:
        return [f"Shape mismatch: {grid1.shape} vs {grid2.shape}"]

    discrepancies = []
    rows, cols = grid1.shape
    for r in range(rows):
        for c in range(cols):
            if grid1[r, c] != grid2[r, c]:
                discrepancies.append(f"Pixel mismatch at ({r},{c}): {grid1[r, c]} vs {grid2[r, c]}")
    return discrepancies

task_data = {
  "train": [
    {
      "input": [[8, 8, 8, 8, 8, 8, 8, 8], [8, 1, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 4, 1, 1, 8], [8, 1, 1, 1, 1, 1, 1, 8], [8, 8, 8, 8, 8, 8, 8, 8]],
      "output": [[8, 8, 8, 8], [8, 1, 1, 8], [8, 1, 4, 8], [8, 1, 1, 8], [8, 8, 8, 8]]
    },
    {
      "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 1, 1, 1, 1, 1, 8, 8, 8], [8, 8, 1, 1, 1, 1, 1, 8, 8, 8], [8, 8, 1, 1, 1, 4, 1, 8, 8, 8], [8, 8, 1, 1, 1, 1, 1, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
      "output": [[8, 8, 8, 8, 8, 8], [8, 8, 1, 1, 8, 8], [8, 8, 1, 1, 8, 8], [8, 8, 1, 4, 8, 8], [8, 8, 1, 1, 8, 8], [8, 8, 8, 8, 8, 8]]
    },
    {
      "input": [[6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 0, 0, 6], [6, 6, 0, 0, 6, 6, 0, 0, 6], [6, 6, 0, 0, 6, 6, 6, 6, 6], [6, 6, 0, 0, 6, 6, 6, 4, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6]],
      "output": [[6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 0, 0, 6], [6, 6, 0, 0, 6, 6, 6], [6, 6, 0, 0, 6, 4, 6], [6, 6, 6, 6, 6, 6, 6]]
    },
    {
      "input": [[0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 4, 0, 0, 0, 3, 0]],
      "output": [[0, 3, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0]]
    }
  ]
}

results = []
for i, example in enumerate(task_data['train']):
    input_grid = example['input']
    expected_output = example['output']
    predicted_output = transform(input_grid)
    discrepancies = compare_grids(predicted_output, expected_output)
    results.append({
        "example": i,
        "input_shape": np.array(input_grid).shape,
        "output_shape": np.array(expected_output).shape,
        "predicted_shape": np.array(predicted_output).shape,
        "discrepancies": discrepancies
    })

for r in results:
    print(r)