# d8c310e9 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation identifies a colored region within the grid and performs a horizontal reflection of the colored pixels within each row of that region,
appending the mirrored segment to the right. White pixels are unchanged.
"""

import numpy as np

def find_colored_region(grid):
    """
    Finds the bounding box of the colored region (non-white pixels).
    """
    rows, cols = grid.shape
    min_row, max_row = rows, -1
    colored_segments = []

    for r in range(rows):
        start_col = -1
        segment = []
        for c in range(cols):
            if grid[r, c] != 0:
                if start_col == -1:
                    start_col = c
                segment.append((c, grid[r,c]))
            elif start_col != -1:
              colored_segments.append( (r, segment) )
              segment = []
              start_col = -1

        if start_col != -1:
             colored_segments.append( (r, segment) )

    return colored_segments

def reflect_and_append(row_segment):

    row_index = row_segment[0]
    segment = row_segment[1]

    if not segment:
      return []
    
    mirrored_segment = segment[::-1]  # Reverse the segment

    return (row_index, segment + mirrored_segment)
    

def transform(input_grid):
    """
    Transforms the input grid by horizontally reflecting a colored region.
    """
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Find the colored region
    colored_region = find_colored_region(input_grid)
    
    # Reflect and append each row segment in the colored region
    for row_segment in colored_region:
      reflected_segment = reflect_and_append(row_segment)
      
      row_idx = reflected_segment[0]
      new_pixels = reflected_segment[1]
      
      if not new_pixels:
        continue

      start_col = new_pixels[0][0]
      
      for i in range(len(new_pixels)):
          col_idx = new_pixels[i][0]
          pixel_value = new_pixels[i][1]
              
          if col_idx < cols:  # Ensure within bounds
              output_grid[row_idx, col_idx] = pixel_value

          mirrored_pixel_value = new_pixels[-1-i][1]
          append_at =  len(new_pixels)
          if col_idx + append_at < cols:
            output_grid[row_idx, col_idx + append_at ] = mirrored_pixel_value


    return output_grid
```
