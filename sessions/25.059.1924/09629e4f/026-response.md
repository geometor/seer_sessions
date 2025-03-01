# 09629e4f • 026 • refine_coder

---
```python
"""
The transformation rule can be described as follows:

1.  **Identify Horizontal Lines:** Find all horizontal lines composed entirely of grey (5) pixels.

2.  **Preserve Grey Lines Conditionally:** Grey lines are preserved in the output *only if* they consist of *all* grey pixels across the entire row.  If a grey pixel exists in a row that's not entirely grey, that pixel is *not* preserved.

3. **Process Each Region:** Process the entire input grid as one area, applying the following logic row by row:

    *   Iterate through each row of the input grid.
    *   Within each row, replace non-zero pixels with 0 unless they are part of a row of consistent color, in which case they should be replaced with 5.

4.  **Combine:** The output grid is constructed with grey lines only when they are fully composed of grey and by changing to grey objects that are composed on horizontal rows of the same color.

"""

import numpy as np

def find_horizontal_lines(grid, color=5):
    """Finds rows that are entirely composed of a specified color."""
    lines = []
    for i, row in enumerate(grid):
        if np.all(row == color):
            lines.append(i)
    return lines

def process_row(row):
    """Processes a single row to create its corresponding output."""
    output_row = np.zeros_like(row)

    # Check for full grey lines
    if np.all(row == 5):
        output_row[:] = 5
        return output_row

    # Find stretches of identical, non-zero, non-grey colors.
    
    start = -1
    current_color = 0
    for x, pixel in enumerate(row):
      if pixel != 0 and pixel != 5:
        if start == -1:
          start = x
          current_color = pixel
        elif pixel != current_color:
          #we have a different color now, process what we just saw
          if x - start > 0:
            #more than one pixel, color it grey
            output_row[start:x] = 5
          start = x
          current_color = pixel #reset to current pixel
      elif start != -1:
        #end of this color run, check length
        if x- start > 0:
          output_row[start:x] = 5
        #reset start
        start = -1
        current_color = 0
    #handle the edge case where we ended on a color run
    if start != -1 and current_color != 0 and (len(row) - start > 0) :
          output_row[start:len(row)] = 5

    return output_row
    

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Initialize output grid
    output_grid = np.zeros_like(input_grid)

    # Process each row
    for y, row in enumerate(input_grid):
      output_grid[y] = process_row(row)
    

    return output_grid.tolist()
```
