import numpy as np

def rotate_grid(grid, k):
  """
  Rotates a grid by k * 90 degrees counter-clockwise.

  Args:
    grid: A numpy array representing the grid.
    k: The number of 90-degree counter-clockwise rotations.
       k=0: 0 degrees (identity)
       k=1: 90 degrees counter-clockwise
       k=2: 180 degrees
       k=3: 270 degrees counter-clockwise (90 degrees clockwise)

  Returns:
    A numpy array representing the rotated grid.
  """
  return np.rot90(grid, k=k)

def transform(input_grid):
  """
  Transforms a 4x4 input grid into an 8x8 output grid by arranging four
  rotated versions of the input grid in a 2x2 layout.
  - Top-left: Input grid (0 degrees rotation)
  - Top-right: Input grid rotated 90 degrees counter-clockwise
  - Bottom-left: Input grid rotated 180 degrees
  - Bottom-right: Input grid rotated 90 degrees clockwise (270 degrees counter-clockwise)
  """
  # Convert input list of lists to a numpy array for easier manipulation
  input_np = np.array(input_grid, dtype=int)
  
  # Get dimensions of the input grid
  h, w = input_np.shape
  
  # Calculate dimensions of the output grid
  output_h = 2 * h
  output_w = 2 * w
  
  # Initialize the output grid with zeros (or any default value)
  output_np = np.zeros((output_h, output_w), dtype=int)

  # 1. Top-Left Quadrant: Identity (0 degrees rotation)
  # No rotation needed, just copy the input grid
  output_np[0:h, 0:w] = input_np

  # 2. Top-Right Quadrant: Rotate 90 degrees counter-clockwise (k=1)
  rotated_ccw_90 = rotate_grid(input_np, k=1)
  output_np[0:h, w:output_w] = rotated_ccw_90

  # 3. Bottom-Left Quadrant: Rotate 180 degrees (k=2)
  rotated_180 = rotate_grid(input_np, k=2)
  output_np[h:output_h, 0:w] = rotated_180

  # 4. Bottom-Right Quadrant: Rotate 90 degrees clockwise (k=3 or k=-1)
  rotated_cw_90 = rotate_grid(input_np, k=3) # 270 degrees counter-clockwise
  output_np[h:output_h, w:output_w] = rotated_cw_90
  
  # Convert the final numpy array back to a list of lists
  output_grid = output_np.tolist()

  return output_grid