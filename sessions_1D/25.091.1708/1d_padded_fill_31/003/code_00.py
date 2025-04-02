import numpy as np

def transform(input_grid):
  """
  Transforms the input grid by processing each row independently. 
  For each row, it finds the first and last occurrence of the non-white 
  color in that row and fills the pixels strictly between these occurrences 
  with that same color.
  """
  
  # Ensure input is a numpy array
  input_grid_np = np.array(input_grid)
  
  # Initialize output_grid as a copy of the input grid
  output_grid = input_grid_np.copy()
  
  # Get the number of rows
  num_rows = output_grid.shape[0]
  
  # Iterate through each row
  for r in range(num_rows):
    # Get the current row
    row = output_grid[r, :]
    
    # Find the column indices of all non-white pixels (color != 0) in this row
    non_white_indices = np.where(row != 0)[0]
    
    # Check if there are at least two non-white pixels in the row
    if len(non_white_indices) >= 2:
      # Get the color to fill with (from the first non-white pixel found)
      fill_color = row[non_white_indices[0]]
      
      # Get the index of the first (leftmost) non-white pixel
      start_col = non_white_indices[0]
      
      # Get the index of the last (rightmost) non-white pixel
      end_col = non_white_indices[-1]
      
      # Fill the pixels strictly between start_col and end_col with the fill_color
      # Check if there is actually space between them (end_col must be at least start_col + 2)
      if start_col + 1 < end_col:
          output_grid[r, start_col + 1 : end_col] = fill_color
          
  # Return the modified grid
  return output_grid