def compare_grids(grid1, grid2):
    """Compares two grids and returns a list of discrepancies."""
    discrepancies = []
    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i, j] != grid2[i, j]:
                discrepancies.append(
                    {
                        "row": i,
                        "col": j,
                        "grid1_value": grid1[i, j],
                        "grid2_value": grid2[i, j],
                    }
                )
    return discrepancies
import numpy as np
#Example Data - actual will be provided by the task

example_input_output_pairs = [
    (
        np.array([[0, 0, 0], [0, 8, 0], [0, 0, 0]]),
        np.array([[0, 8, 0], [0, 8, 0], [0, 8, 0]]),
    ),
    (
        np.array([[8, 0, 0], [0, 0, 0], [0, 0, 0]]),
        np.array([[8, 0, 0], [8, 0, 0], [8, 0, 0]]),
    ),
     (
        np.array([[0, 0, 0], [0, 0, 0], [0, 0, 8]]),
        np.array([[0, 0, 8], [0, 0, 8], [0, 0, 8]]),
    ),
]

for i, (input_grid, output_grid) in enumerate(example_input_output_pairs):

  predicted_output = transform(input_grid)  #using previously defined transform function
  discrepancies = compare_grids(predicted_output, output_grid)

  print(f"Example {i + 1}:")
  print(f"  Input Dimensions: {input_grid.shape}")
  print(f"  Output Dimensions: {output_grid.shape}")
  print(f"  Azure Pixel Locations (Input): {np.argwhere(input_grid == 8).tolist()}")
  print(f"  Discrepancies: {discrepancies}")