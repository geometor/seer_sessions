# 7c008303 • 019 • refine_coder

---
```python
"""
Transforms the input grid to output grid based on color mapping and position.

1. **Initialization:** Create an output grid of size 6x6, initialized with all zeros (white).
2. **Color Mapping:**  Use a predefined color map to translate input colors to output colors. The map is as follows:
      - Input 8 (azure) maps to Output 2 (red) and 4 (yellow).
      - Input 3 (green) maps to Output 5 (gray) and 6 (magenta).
      - Input 2 (red) maps to Output 2 (red).
      - Input 4 (yellow) maps to Output 4 (yellow).
      - Input 6 (magenta) maps to Output 6 (magenta).
      - Input 1 has no output colors.
      - Input 5 (gray) maps to 5 (gray)

3. **Spatial Transformation:**
      - Check the input colors, if input color 8 (azure) exists, place output color 2 (red) in the output grid's first column (column 0), and output color 4 (yellow) in the output grid last column(column 5). The rows are defined by the rows where color 8 first appears in the second and last column of the input grid.
      - For other input colors, their positions in the input grid directly correspond to their positions in the output grid, but input rows and columns are module 6.
      - If input color does not exists the output remains 0.
"""

import numpy as np

def get_positions(grid, color):
    """
    Returns a list of (row, col) tuples representing the positions of a given color in the grid.
    """
    return [(row, col) for row in range(grid.shape[0]) for col in range(grid.shape[1]) if grid[row, col] == color]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((6, 6), dtype=int)

    # Color Position Mapping and Dimension Reduction
    color_map = {
      8 : [2,4],
      3 : [5,6],
      2 : [2],
      4 : [4],
      6 : [6],
      5 : [5]
    }

    input_positions = {}

    for color in color_map:
        input_positions[color] = get_positions(input_grid, color)

    # build output based on relative locations
    # iterate through color_map and their corresponding input positions
    # calculate target positions in output
    for color, output_colors in color_map.items():
        if len(input_positions[color])>0:
            if color == 8:  # Handle azure (8)
                
                # first occurance of 8
                # find all columns where 8 is present
                cols_with_8 = sorted(list(set([pos[1] for pos in input_positions[8]])))
                if len(cols_with_8) > 0:
                    first_col_with_8 = cols_with_8[0]
                    first_occurance = [pos for pos in input_positions[8] if pos[1] == first_col_with_8][0]
                    output_row_8_1 = first_occurance[0] if first_occurance[0] < 6 else first_occurance[0] % 6
                    output_grid[output_row_8_1,0] = output_colors[0]

                    # second occurance of 8
                    last_col_with_8 = cols_with_8[-1]
                    second_occurance = [pos for pos in input_positions[8] if pos[1] == last_col_with_8][0]
                    output_row_8_2 =  second_occurance[0] if second_occurance[0] < 6 else second_occurance[0] % 6
                    output_grid[output_row_8_2, 5] = output_colors[1]
            
            
            else: #remaining colors
                for pos in input_positions[color]:
                    if pos[0] < 6 and pos[1] < 6:
                        output_grid[pos[0], pos[1]] = output_colors[0]


    return output_grid
```
