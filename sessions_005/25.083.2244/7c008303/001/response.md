```python
"""
Transforms an input grid into a smaller output grid by extracting and combining colored regions from above and below a horizontal azure (8) line.
"""

import numpy as np

def get_azure_line_row(grid):
    """Finds the row index of the horizontal azure line."""
    for i, row in enumerate(grid):
        if all(pixel == 8 for pixel in row):
            return i
    return -1  # Should not happen given the task description

def extract_colored_columns(grid_section):
    """
    Extracts colored (non-white, non-azure) pixel regions column-wise.
    Returns a list of lists, where each sublist represents a column's colored pixels.
    """
    
    num_cols = grid_section.shape[1]
    colored_columns = []

    for j in range(num_cols):
        col = grid_section[:, j]
        colored_pixels = [pixel for pixel in col if pixel != 0 and pixel != 8]
        if colored_pixels:
            colored_columns.append(colored_pixels)

    return colored_columns
  

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    input_grid = np.array(input_grid)  # Ensure input is a NumPy array
    azure_line_row = get_azure_line_row(input_grid)

    # Separate the grid into sections above and below the azure line
    top_section = input_grid[:azure_line_row]
    bottom_section = input_grid[azure_line_row + 1:]

    # Extract colored columns from each section
    top_colored_columns = extract_colored_columns(top_section)
    bottom_colored_columns = extract_colored_columns(bottom_section)

    # Determine the output grid dimensions
    
    #get all the unique, non-zero, non-eight elements
    top_cols = len(top_colored_columns)
    bottom_cols = len(bottom_colored_columns)
    max_cols = max(top_cols,bottom_cols)

    top_rows = sum(len(col) for col in top_colored_columns) # Count total elements across the lists
    bottom_rows = sum(len(col) for col in bottom_colored_columns) # Count total elements across the lists

    output_height = max(top_rows,bottom_rows)
    output_width = max_cols
    if output_height > 0 and output_width > 0:
        output_grid = np.zeros((output_height, output_width), dtype=int)
    else:
       return []
    # Build the output grid
    
    
    # Populate the top section of the output grid
    col_idx = 0
    row_idx = 0

    for col in top_colored_columns:
      for pixel in col:
        output_grid[row_idx,col_idx] = pixel
      row_idx += 1
      if row_idx >= top_rows:
        col_idx +=1
        row_idx = 0

    # Populate the bottom section of the output grid
    col_idx = 0
    row_idx = 0

    offset = top_rows

    if(bottom_rows > 0 ):
        output_grid = np.concatenate([output_grid,np.zeros((bottom_rows,output_width),dtype=int)])
        
    for col in bottom_colored_columns:
      for pixel in col:
          output_grid[row_idx + offset, col_idx] = pixel
      row_idx +=1
      if row_idx >= bottom_rows:
        col_idx += 1
        row_idx = 0

    return output_grid.tolist()
```