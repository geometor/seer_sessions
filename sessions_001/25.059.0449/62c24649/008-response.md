# 62c24649 • 008 • refine_coder

---
```tool_code
"""
The output grid is created by horizontally duplicating the input grid, adjusting for width and potentially changing the color.
- If the input grid is entirely gray (color 5), the output grid is created by duplicating the input grid horizontally.
- If the input grid contains all the same color:
  - and if the input height * 2 -1 equals the output height and the width is the same
      set output to all 1s
  - and if the input width * 2 - 1 equals the output width
      copy the input and extend it
  - if none of above is true - simple duplicate the input grid
"""

import numpy as np

def transform(input_grid):
    # Get input dimensions
    input_height, input_width = input_grid.shape
    unique_colors = np.unique(input_grid)

    
    if np.all(input_grid == 5):
      # Duplicate horizontally
      output_grid = np.tile(input_grid, 2)
        
    elif len(unique_colors) == 1:
        if input_height * 2 - 1 == output_grid.shape[0] and input_width * 2 -1 == output_grid.shape[1]:
            output_grid = np.ones((input_height * 2 -1, input_width * 2 - 1), dtype=int)
        
        elif input_width * 2 - 1 == output_grid.shape[1]:
            output_grid = np.hstack((input_grid, input_grid[:, :-1]))

        else:
          output_grid = np.tile(input_grid, 2)
    else:
      output_grid = np.tile(input_grid, 2)

    return output_grid
```
