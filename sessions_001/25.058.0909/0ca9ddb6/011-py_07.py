def compare_grids(grid1, grid2):
    """Compares two grids and returns a detailed report."""
    comparison = (grid1 == grid2)
    differences = np.argwhere(~comparison)
    report = {
        "match": np.all(comparison),
        "differences": []
    }
    for row, col in differences:
      report["differences"].append(
          {
              "location": (int(row), int(col)),
              "grid1_value": int(grid1[row, col]),
              "grid2_value": int(grid2[row, col])
          })
    return report

# Example for a single training example (assuming I have the data).  The data shown here is illustrative only, and not the true data from any ARC task.
input_grid = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 0, 8, 0],
    [0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

output_grid = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 7, 8, 0],
    [0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0]
])
predicted_output = transform(input_grid)

comparison_result = compare_grids(output_grid, predicted_output)
print(f"Example Comparison Report:\n{comparison_result}")
