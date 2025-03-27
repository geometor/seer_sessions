import numpy as np

def rotate_subgrid_clockwise(subgrid):
  """Rotates a 2D numpy array 90 degrees clockwise."""
  return np.rot90(subgrid, k=-1)

def rotate_subgrid_180(subgrid):
  """Rotates a 2D numpy array 180 degrees."""
  return np.rot90(subgrid, k=-2)

def transform(input_grid):
  """
  Transforms the input grid based on the observed pattern.

  The input grid is divided conceptually by gray vertical lines (column 3 and 7).
  The 3x3 block in columns 0-2 (the "Source Block") is identified.
  The Source Block is rotated 90 degrees clockwise and placed in columns 4-6.
  The Source Block is rotated 180 degrees and placed in columns 8-10.
  The rest of the grid (columns 0-3 and column 7) remains unchanged.
  """
  # Convert the input list of lists to a numpy array for easier manipulation
  input_array = np.array(input_grid, dtype=int)

  # Initialize the output grid as a copy of the input grid
  output_array = np.copy(input_array)

  # Define the coordinates for the source block
  source_rows = slice(0, 3)
  source_cols = slice(0, 2 + 1) # Slice goes up to, but not including, the end index

  # Extract the Source Block
  source_block = input_array[source_rows, source_cols]

  # --- Transformation Step 1: Rotate 90 degrees clockwise ---
  # Rotate the source block 90 degrees clockwise
  rotated_90 = rotate_subgrid_clockwise(source_block)

  # Define the coordinates for the first target area
  target1_rows = slice(0, 3)
  target1_cols = slice(4, 6 + 1)

  # Place the 90-degree rotated block into the output grid
  output_array[target1_rows, target1_cols] = rotated_90

  # --- Transformation Step 2: Rotate 180 degrees ---
  # Rotate the original source block 180 degrees
  rotated_180 = rotate_subgrid_180(source_block)

  # Define the coordinates for the second target area
  target2_rows = slice(0, 3)
  target2_cols = slice(8, 10 + 1)

  # Place the 180-degree rotated block into the output grid
  output_array[target2_rows, target2_cols] = rotated_180

  # Convert the output numpy array back to a list of lists
  output_grid = output_array.tolist()

  return output_grid