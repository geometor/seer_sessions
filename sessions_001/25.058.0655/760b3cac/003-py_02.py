import numpy as np

def code_execution(input_grid):
    rows, cols = input_grid.shape
    azure_objects = get_objects(input_grid, 8)

    row_data = {}
    for row_index in range(min(3, rows)):  # Only consider the top 3 rows
        row_data[row_index] = {
            "has_azure": False,
            "leftmost_azure_col": cols,  # Initialize to the maximum possible column index
            "azure_pixels":[]
        }

    for obj in azure_objects:
        for r, c in obj:
            if r < 3:  # Within the top 3 rows
                row_data[r]["has_azure"] = True
                row_data[r]["leftmost_azure_col"] = min(row_data[r]["leftmost_azure_col"], c)
                row_data[r]["azure_pixels"].append((r,c))

    return row_data

# input grids - from the previous turn
examples = [
    np.array([[4, 4, 4, 4, 4, 4, 4, 4, 4],
       [4, 4, 4, 8, 4, 4, 4, 4, 4],
       [4, 4, 4, 4, 4, 4, 8, 4, 4],
       [4, 4, 4, 4, 4, 4, 4, 4, 4]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [8, 0, 0, 0, 0, 0, 0, 0, 8, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[6, 8, 6, 5, 8, 0, 0, 6, 0],
        [0, 6, 8, 0, 0, 4, 0, 0, 4],
        [0, 0, 0, 6, 0, 8, 4, 0, 0],
        [0, 0, 6, 6, 0, 4, 4, 0, 0]])
]

for i, input_grid in enumerate(examples):
  row_data = code_execution(input_grid)
  print(f"Example {i+1}:")
  for row_index, data in row_data.items():
      print(f"  Row {row_index}:")
      print(f"    Has Azure: {data['has_azure']}")
      if data['has_azure']:
          print(f"    Leftmost Azure Column: {data['leftmost_azure_col']}")
          print(f"    Azure Pixels: {data['azure_pixels']}")