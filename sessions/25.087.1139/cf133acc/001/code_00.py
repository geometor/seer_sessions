import numpy as np

def transform(input_grid):
  """
  Finds white pixels (0) that are horizontally surrounded by the same non-white color.
  Specifically, if a pixel at (r, c) is white (0), and its left neighbor (r, c-1) 
  and right neighbor (r, c+1) are both the same color C (where C > 0), 
  then the pixel (r, c) in the output grid is changed to color C.
  All other pixels remain unchanged.
  """
  # Convert input list of lists to a numpy array for easier slicing and manipulation
  input_np = np.array(input_grid, dtype=int)
  # Create a copy to modify, preserving the original input for checks
  output_grid = input_np.copy()
  # Get the dimensions of the grid
  height, width = input_np.shape

  # Iterate through each pixel in the grid
  # We only need to check pixels that have both a left and a right neighbor,
  # so the column index 'c' ranges from 1 to width-2.
  for r in range(height):
      for c in range(1, width - 1):
          # Check if the current pixel is white (color code 0)
          if input_np[r, c] == 0:
              # Get the colors of the left and right neighbors
              left_neighbor_color = input_np[r, c-1]
              right_neighbor_color = input_np[r, c+1]

              # Check if the neighbors have the same color and are not white
              if left_neighbor_color == right_neighbor_color and left_neighbor_color != 0:
                  # If the conditions are met, change the color of the current pixel 
                  # in the output grid to the color of its neighbors
                  output_grid[r, c] = left_neighbor_color

  # Convert the final numpy array back to a list of lists before returning
  return output_grid.tolist()