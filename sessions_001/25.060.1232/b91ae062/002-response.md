# b91ae062 • 002 • example_5 • investigate_coder

---
```python
"""
The transformation rule is to replicate each non-background pixel in the input grid into a rectangular block in the output grid. The size of each block is determined by a replication factor, which can be different for each input. The remaining cells in the output grid are filled with the background color (0).
"""

import numpy as np

def get_replication_factor(input_grid, output_grid):
    # Calculate the replication factor for rows and columns
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape

    row_factor = output_rows // input_rows
    col_factor = output_cols // input_cols

    #Check to make sure a single factor applied to all
    for r in range(input_rows):
      for c in range(input_cols):
          if input_grid[r,c] != 0:
              count = np.count_nonzero(output_grid == input_grid[r,c])
              if row_factor * col_factor != count / (np.count_nonzero(input_grid == input_grid[r,c])):
                return "Variable"
                

    return row_factor, col_factor

def transform(input_grid, output_grid):

    # Calculate output grid size and initialize
    input_rows, input_cols = input_grid.shape

    factor = get_replication_factor(input_grid, output_grid)

    if factor == "Variable": #Variable expansion factor per pixel
        output_rows, output_cols = output_grid.shape
        output_grid_new = np.zeros((output_rows, output_cols), dtype=int)
        row_cursor = 0
        col_cursor = 0

        for r in range(input_rows):
          col_cursor = 0
          for c in range(input_cols):
            if input_grid[r,c] != 0:
              color_count = np.count_nonzero(output_grid == input_grid[r,c])
              color_block = np.array(np.where(output_grid == input_grid[r,c])).T
              h = max(color_block[:,0]) - min(color_block[:,0]) + 1
              w = max(color_block[:,1]) - min(color_block[:,1]) + 1
              
              for i in range(h):
                for j in range(w):
                  output_grid_new[row_cursor + i, col_cursor + j ] = input_grid[r,c]

              col_cursor += w
            else:
              pass
          row_cursor += h
        
    else:
        row_factor, col_factor = factor

        output_rows = input_rows * row_factor
        output_cols = input_cols * col_factor
        output_grid_new = np.zeros((output_rows, output_cols), dtype=int)


        # Iterate and replicate
        for r in range(input_rows):
            for c in range(input_cols):
                color = input_grid[r, c]
                if color != 0:  # Replicate only non-background pixels
                    for i in range(row_factor):
                        for j in range(col_factor):
                            output_grid_new[r * row_factor + i, c * col_factor + j] = color

    return output_grid_new
```
