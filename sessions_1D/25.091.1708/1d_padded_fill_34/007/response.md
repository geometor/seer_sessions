```python
import numpy as np

"""
Fill horizontal segments in each row, bounded by the first (leftmost) and 
last (rightmost) non-background pixels found in that row of the input grid. 
The background color is assumed to be white (0). The single non-background 
color present in the input is used for filling the segments. Rows 
containing only the background color remain unchanged.
"""

def find_non_background_color(grid_np):
  """
  Identifies the single non-background color present in the grid.
  Assumes exactly one non-background color exists besides the background (0).

  Args:
    grid_np: A NumPy array representing the input grid.

  Returns:
    The integer value of the non-background color, or 0 if only background 
    color is found.
  """
  # Get unique color values present in the grid
  unique_colors = np.unique(grid_np)
  # Iterate through unique colors to find the one that isn't background (0)
  for color in unique_colors:
    if color != 0:
      return color
  # If only background color (0) is found, return 0
  return 0

def transform(input_grid):
    """
    Applies the horizontal segment filling transformation to the input grid.

    Args:
      input_grid: A list of lists representing the input grid.

    Returns:
      A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize the output grid with the background color (white, 0)
    # It will have the same dimensions as the input grid.
    output_grid_np = np.zeros_like(input_grid_np)

    # Identify the single non-background color used in the input grid
    fill_color = find_non_background_color(input_grid_np)

    # If the input grid only contains the background color, return the all-white output grid
    if fill_color == 0:
        return output_grid_np.tolist() 

    # Process each row independently
    for r in range(height):
        # Get the current row from the input grid
        row = input_grid_np[r, :]
        
        # Find the column indices where the non-background color appears in this row
        # np.where returns a tuple, we need the first element (the array of indices)
        indices = np.where(row == fill_color)[0]

        # Check if the non-background color was found in the current row
        if len(indices) > 0:
            # Determine the start (leftmost) and end (rightmost) columns for the segment
            start_col = np.min(indices)
            end_col = np.max(indices)

            # Fill the segment in the corresponding row of the output grid
            # Slicing output_grid_np[r, start_col:end_col+1] selects the columns
            # from start_col up to (but not including) end_col + 1.
            output_grid_np[r, start_col : end_col + 1] = fill_color
        
        # If the non-background color is not found in the row (len(indices) == 0), 
        # the output row remains initialized as all background color (0), 
        # so no specific action is needed for that row.

    # Convert the final NumPy array back to a list of lists for the required output format
    return output_grid_np.tolist()
```