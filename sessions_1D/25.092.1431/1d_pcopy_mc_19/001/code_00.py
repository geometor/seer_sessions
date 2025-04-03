import numpy as np

def transform(input_grid):
  """
  Identifies single, isolated non-white pixels in the input grid and expands them
  horizontally to the right to form a 1x3 line of the same color. Pixels that
  are already part of a larger non-white object or are background (white) remain
  unchanged. A pixel is considered isolated if its four cardinal neighbors
  (up, down, left, right) are either background (0) or outside the grid boundaries.
  """

  # Convert input list of lists to a numpy array for easier manipulation
  input_array = np.array(input_grid, dtype=int)
  # Create a deep copy to modify and return as the output
  output_array = np.copy(input_array)
  height, width = input_array.shape

  # Iterate through each cell (pixel) of the input grid
  for r in range(height):
    for c in range(width):
      color = input_array[r, c]

      # Check if the pixel is non-white (not 0)
      if color != 0:
        # Check if the pixel is isolated (1x1 object)
        is_isolated = True

        # Check left neighbor
        if c > 0 and input_array[r, c - 1] == color:
          is_isolated = False
        # Check right neighbor
        if c < width - 1 and input_array[r, c + 1] == color:
          is_isolated = False
        # Check top neighbor
        if r > 0 and input_array[r - 1, c] == color:
          is_isolated = False
        # Check bottom neighbor
        if r < height - 1 and input_array[r + 1, c] == color:
          is_isolated = False

        # If the pixel is isolated, expand it horizontally to the right in the output grid
        if is_isolated:
          # The original pixel keeps its color (already copied)
          # Expand to the right by two pixels, checking boundaries
          if c + 1 < width:
            output_array[r, c + 1] = color
          if c + 2 < width:
            output_array[r, c + 2] = color

  # Convert the numpy array back to a list of lists for the standard ARC format
  return output_array.tolist()