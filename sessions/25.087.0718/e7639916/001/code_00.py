import numpy as np

def find_pixels(grid, color):
  """Finds all coordinates of pixels with a specific color."""
  rows, cols = np.where(grid == color)
  return list(zip(rows, cols))

def transform(input_grid):
  """
  Draws a blue (1) rectangular frame around the bounding box of all azure (8) pixels
  found in the input grid. The frame is drawn only on white (0) background pixels,
  preserving the original azure pixels if they lie on the frame's path.
  """
  # Convert the input list of lists to a NumPy array for easier manipulation
  input_np = np.array(input_grid, dtype=int)
  output_grid = np.copy(input_np)
  
  # Find the coordinates of all azure (8) pixels
  azure_pixels = find_pixels(input_np, 8)
  
  # If there are no azure pixels, return the original grid
  if not azure_pixels:
      return input_grid # Or output_grid.tolist() if consistency is needed
      
  # Determine the bounding box coordinates
  rows = [r for r, c in azure_pixels]
  cols = [c for r, c in azure_pixels]
  min_row = min(rows)
  max_row = max(rows)
  min_col = min(cols)
  max_col = max(cols)
  
  # Draw the top edge of the frame
  for c in range(min_col, max_col + 1):
      if output_grid[min_row, c] == 0: # Check if pixel is white
          output_grid[min_row, c] = 1 # Draw blue
          
  # Draw the bottom edge of the frame
  for c in range(min_col, max_col + 1):
      if output_grid[max_row, c] == 0: # Check if pixel is white
          output_grid[max_row, c] = 1 # Draw blue
          
  # Draw the left edge of the frame
  for r in range(min_row, max_row + 1): # Iterate through rows within the bounds
      if output_grid[r, min_col] == 0: # Check if pixel is white
          output_grid[r, min_col] = 1 # Draw blue
          
  # Draw the right edge of the frame
  for r in range(min_row, max_row + 1): # Iterate through rows within the bounds
      if output_grid[r, max_col] == 0: # Check if pixel is white
          output_grid[r, max_col] = 1 # Draw blue

  # Convert the NumPy array back to a list of lists for the final output
  return output_grid.tolist()