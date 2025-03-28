import numpy as np

def rot90_ccw(grid_np):
  """Rotates a numpy array 90 degrees counter-clockwise."""
  return np.rot90(grid_np, k=1)

def rot180(grid_np):
  """Rotates a numpy array 180 degrees."""
  return np.rot90(grid_np, k=2)

def rot270_ccw(grid_np):
  """Rotates a numpy array 270 degrees counter-clockwise (or 90 clockwise)."""
  return np.rot90(grid_np, k=3)

def transform(input_grid):
  """
  Transforms the input grid by creating a 2x2 tiled output grid.
  The top-left tile is the original input grid.
  The top-right tile is the input grid rotated 90 degrees counter-clockwise.
  The bottom-left tile is the input grid rotated 180 degrees.
  The bottom-right tile is the input grid rotated 270 degrees counter-clockwise.
  """
  # Convert input list of lists to a numpy array for easier manipulation
  input_np = np.array(input_grid, dtype=int)
  
  # Get the dimensions of the input grid
  height, width = input_np.shape
  
  # Calculate the dimensions of the output grid (twice the input dimensions)
  output_height = height * 2
  output_width = width * 2
  
  # Initialize the output grid with zeros (or any default value, it will be overwritten)
  output_np = np.zeros((output_height, output_width), dtype=int)
  
  # Calculate the rotated versions of the input grid using numpy's rot90
  # np.rot90 rotates counter-clockwise
  grid_rot0 = input_np               # 0 degrees rotation (original)
  grid_rot1 = rot90_ccw(input_np)    # 90 degrees counter-clockwise
  grid_rot2 = rot180(input_np)       # 180 degrees rotation
  grid_rot3 = rot270_ccw(input_np)   # 270 degrees counter-clockwise (or 90 clockwise)

  # Place the original and rotated grids into the corresponding quadrants of the output grid
  # Top-left quadrant (0 degrees)
  output_np[0:height, 0:width] = grid_rot0
  
  # Top-right quadrant (90 degrees CCW)
  output_np[0:height, width:output_width] = grid_rot1
  
  # Bottom-left quadrant (180 degrees)
  output_np[height:output_height, 0:width] = grid_rot2
  
  # Bottom-right quadrant (270 degrees CCW)
  output_np[height:output_height, width:output_width] = grid_rot3
  
  # Convert the output numpy array back to a list of lists
  output_grid = output_np.tolist()
  
  return output_grid
