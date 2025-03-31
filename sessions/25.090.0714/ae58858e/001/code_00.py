import numpy as np

def transform(input_grid):
  """
  Transforms the input grid based on the following rule:
  1. Identify all occurrences of 2x2 squares composed entirely of red (2) pixels in the input grid.
  2. For every red (2) pixel that is part of at least one such 2x2 red square, change its color to magenta (6) in the output grid.
  3. All other pixels (white (0) or red (2) pixels not part of a 2x2 red square) remain unchanged.
  """
  # Convert input list of lists to a NumPy array for efficient operations
  input_np = np.array(input_grid, dtype=int)
  # Initialize the output grid as a copy of the input grid
  output_np = np.copy(input_np)
  
  # Get the dimensions of the grid
  height, width = input_np.shape

  # Iterate through all possible top-left corners (r, c) of a 2x2 square
  # The loops stop at height-1 and width-1 because a 2x2 square needs indices r, r+1 and c, c+1
  for r in range(height - 1):
      for c in range(width - 1):
          # Define the coordinates of the four pixels in the potential 2x2 square
          top_left = (r, c)
          top_right = (r, c + 1)
          bottom_left = (r + 1, c)
          bottom_right = (r + 1, c + 1)

          # Check if all four pixels in the input grid are red (2)
          if (input_np[top_left] == 2 and
              input_np[top_right] == 2 and
              input_np[bottom_left] == 2 and
              input_np[bottom_right] == 2):
              
              # If they form a 2x2 red square, change the corresponding
              # four pixels in the output grid to magenta (6)
              output_np[top_left] = 6
              output_np[top_right] = 6
              output_np[bottom_left] = 6
              output_np[bottom_right] = 6
              
  # Convert the NumPy array back to a list of lists for the final output
  output_grid = output_np.tolist()
  
  return output_grid