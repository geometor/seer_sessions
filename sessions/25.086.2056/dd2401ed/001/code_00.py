import numpy as np

def find_vertical_line_column(grid, color):
  """Finds the column index of a solid vertical line of a specific color."""
  grid_np = np.array(grid)
  height, width = grid_np.shape
  for c in range(width):
    if np.all(grid_np[:, c] == color):
      return c
  # Fallback if not a solid line, find first occurrence in first row
  for c in range(width):
      if grid_np[0, c] == color:
          return c
  return -1 # Should not happen based on examples

def count_pixels(grid, color):
  """Counts the occurrences of a specific color in the grid."""
  grid_np = np.array(grid)
  return np.count_nonzero(grid_np == color)

def transform(input_grid):
  """
  Transforms the input grid based on the following rule:
  1. Identify the vertical gray (5) line in the input grid.
  2. Count the total number of red (2) pixels in the input grid.
  3. Create the output grid by copying the input grid.
  4. Erase the original gray line in the output grid, setting its column to white (0).
  5. Draw a new gray line in the output grid, shifted to the right by a number of columns equal to the count of red pixels. This new line overwrites existing pixels.
  All other pixels (blue, red, white) retain their original positions unless overwritten by the moved gray line.
  """
  
  input_grid_np = np.array(input_grid, dtype=int)
  output_grid_np = np.copy(input_grid_np)
  height, width = input_grid_np.shape
  
  # Define colors
  GRAY = 5
  RED = 2
  WHITE = 0
  
  # 1. Find the column index of the gray line
  gray_col_in = -1
  for c in range(width):
      # Check if the entire column is gray (more robust)
      is_solid_gray_line = True
      for r in range(height):
          if input_grid_np[r, c] != GRAY:
              is_solid_gray_line = False
              break
      if is_solid_gray_line:
          gray_col_in = c
          break
          
  # Fallback if no solid gray line found (as seen in some examples where other colors might be in the gray column)
  # Find first instance of gray in any row if solid line check fails
  if gray_col_in == -1:
       for r in range(height):
           for c in range(width):
               if input_grid_np[r,c] == GRAY:
                   # Assume it's a vertical line even if not solid
                   gray_col_in = c 
                   break
           if gray_col_in != -1:
               break

  if gray_col_in == -1:
      # Handle error case where no gray pixel is found
      # Based on task description, this shouldn't happen
      return input_grid # Or raise an error

  # 2. Count the number of red pixels
  num_red_pixels = np.count_nonzero(input_grid_np == RED)
  
  # 3. Calculate the destination column for the gray line
  gray_col_out = gray_col_in + num_red_pixels
  
  # Ensure the destination column is within bounds (although examples suggest it won't exceed)
  if gray_col_out >= width:
      # Behavior not specified for out-of-bounds, assume it stops at the edge or error?
      # Based on examples, let's assume it stays within bounds.
      # If an error case needed handling, it would go here.
      # For now, let it proceed, potentially causing index error if out of bounds
      # Or clamp it: gray_col_out = width - 1
      pass # Assume valid based on examples

  # 4. Erase the original gray line column in the output grid
  # Only change pixels that were originally gray to white.
  # Other pixels in that column should remain.
  for r in range(height):
      if output_grid_np[r, gray_col_in] == GRAY:
           output_grid_np[r, gray_col_in] = WHITE
           
  # 5. Draw the new gray line in the output grid
  # This overwrites whatever is currently in the destination column.
  if 0 <= gray_col_out < width:
      for r in range(height):
          output_grid_np[r, gray_col_out] = GRAY
          
  # Convert back to list of lists if necessary for the environment
  output_grid = output_grid_np.tolist()
  
  return output_grid
