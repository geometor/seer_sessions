# 0d3d703e • 012 • refine_coder

---
```python
"""
The transformation rule performs a selective color mapping based on the presence of specific color patterns.  The input and output grids have the same dimensions. The color changes only occur in the first example. In the other examples, all the colors are present but the color changes do not occur. The color changes are:

1.  Red (2) is replaced with Magenta (6).
2.  Green (3) is replaced with Yellow (4).
3.  Azure (8) is replaced with Maroon (9).

The color changes may be dependent on all colors being present in the input grid and/or the specific shape/configuration of colors in the input.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input.
    output_grid = np.copy(input_grid)

    # Define the color mapping.
    color_map = {
        2: 6,  # Red to Magenta
        3: 4,  # Green to Yellow
        8: 9   # Azure to Maroon
    }
    
    # Check if all colors to be mapped are present. This isn't sufficient, but is necessary
    all_colors_present = all(color in input_grid for color in color_map)
    
    # Apply color changes for example 1, by checking that the colors are present.
    if all_colors_present:
        # Iterate through each pixel in the grid.
        for i in range(input_grid.shape[0]):
            for j in range(input_grid.shape[1]):
                # Get the color of the current pixel.
                current_color = input_grid[i, j]

                # Apply color mapping if the current color is in the map.
                if current_color in color_map:
                    output_grid[i, j] = color_map[current_color]

    return output_grid
```

