import numpy as np

def transform(input_grid):
  """
  Transforms the input grid by rotating it 180 degrees around its center.

  The transformation involves the following steps:
  1. Convert the input list of lists into a NumPy array.
  2. Use NumPy's rot90 function twice to achieve a 180-degree rotation.
  3. Convert the resulting NumPy array back into a list of lists format.
  """

  # Convert the input list of lists to a NumPy array for easier manipulation
  input_grid_np = np.array(input_grid, dtype=int)

  # Rotate the NumPy array 180 degrees (equivalent to two 90-degree rotations)
  # k=2 specifies the number of 90-degree counter-clockwise rotations.
  output_grid_np = np.rot90(input_grid_np, k=2)

  # Convert the rotated NumPy array back to a list of lists
  output_grid = output_grid_np.tolist()

  return output_grid