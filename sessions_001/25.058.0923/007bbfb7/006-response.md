# 007bbfb7 • 006 • refine_coder

---
```python
"""
The output grid's dimensions are determined by multiplying each of the input dimensions by a factor. The x dimension is multiplied by the input's x dimension plus 1. The y dimension is multiplied by the input's y dimension plus 1. The output grid consists of vertical stripes. The first few stripes are white (0). The remaining stripes have the same color as the non-zero color in the input, and the number of these colored stripes corresponds to the number of cells along one side of the input grid. When an input dimension is 2, then instead of the number of white stripes being the input's related dimension value it is that value plus one.
"""

import numpy as np

def transform(input_grid):
    # Determine output grid dimensions.
    input_shape = input_grid.shape
    output_height = input_shape[0] * 3
    output_width = input_shape[1] * 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Find the non-zero color in the input grid.
    non_zero_colors = [color for color in np.unique(input_grid) if color != 0]
    if len(non_zero_colors) > 0:
        fill_color = non_zero_colors[0]
    else:
        fill_color = 0

    # Create vertical stripes.

    # determine the number of white stripes
    # special case rule for dimension of 2, use width to determine
    if input_shape[1] == 2:
       num_white_stripes = input_shape[1] + 1
    else:
      num_white_stripes = input_shape[1]

    for j in range(output_width):
        # determine which stripe
        stripe_index_w = j // input_shape[1] if input_shape[1] != 2 else j // (input_shape[1]+1)

        # fill columns with white, or fill color
        if stripe_index_w < 1:
           output_grid[:, j] = 0
        else:
           output_grid[:, j] = fill_color
           

    return output_grid
```
