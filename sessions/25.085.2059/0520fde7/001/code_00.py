import numpy as np

def find_separator_column(grid):
  """
    Finds the index of the first column consisting entirely of a single, non-background color.
    In this task, it specifically looks for the gray (5) column.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The index of the separator column, or -1 if not found.
    """
  height, width = grid.shape
  for c in range(width):
        # Check if all elements in the column are the same and not background (0)
        # In this specific task, we know it's gray (5)
        if np.all(grid[:, c] == 5):
            return c
  return -1 # Should not happen based on task description

def transform(input_grid):
  """
    Transforms the input grid based on the following rule:
    1. Identifies a central vertical separator line (gray color 5).
    2. Creates an output grid with the same height as the input and width equal 
       to the number of columns to the left of the separator.
    3. Initializes the output grid with white pixels (0).
    4. Iterates through each cell (r, c) to the left of the separator in the input grid.
    5. Checks if the cell (r, c) contains a blue pixel (1) AND the corresponding
       symmetrically mirrored cell across the separator (r, separator_index + 1 + c)
       also contains a blue pixel (1).
    6. If both conditions are true, the corresponding cell (r, c) in the output grid 
       is set to red (2). Otherwise, it remains white (0).
    """

  # Convert input list of lists to numpy array for easier slicing and checks
  input_np = np.array(input_grid, dtype=int)
  height, width = input_np.shape

  # Find the gray separator column index
  # Based on examples, it's always column 3, but finding it dynamically is more robust.
  gray_col_index = find_separator_column(input_np)

  # Handle case where separator might not be found (though examples guarantee it)
  if gray_col_index == -1:
      raise ValueError("Gray separator column (color 5) not found in the input grid.")

  # Determine output grid dimensions
  # Output height is same as input height.
  output_height = height
  # Output width is the number of columns to the left of the separator.
  output_width = gray_col_index

  # Initialize output grid with white (0)
  output_grid = np.zeros((output_height, output_width), dtype=int)

  # Iterate through rows and columns of the potential output grid
  # (which corresponds to the left side of the input grid)
  for r in range(output_height):
      for c in range(output_width):
          # Calculate the corresponding column index on the right side of the separator
          # The reflection is relative to the separator column
          right_col_index = gray_col_index + 1 + c

          # Ensure the right_col_index is within the bounds of the input grid width
          if right_col_index < width:
              # Check the symmetry condition:
              # Is the pixel at (r, c) blue (1)?
              is_left_blue = (input_np[r, c] == 1)
              # Is the mirrored pixel at (r, right_col_index) blue (1)?
              is_right_blue = (input_np[r, right_col_index] == 1)

              # If both the left pixel and its mirrored right pixel are blue...
              if is_left_blue and is_right_blue:
                  # ...set the corresponding output pixel to red (2)
                  output_grid[r, c] = 2
          # Otherwise, the output pixel remains white (0) as initialized

  # Convert the final numpy array back to a list of lists for the expected output format
  return output_grid.tolist()