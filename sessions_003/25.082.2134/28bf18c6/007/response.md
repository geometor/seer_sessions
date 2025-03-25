```python
"""
1.  **Bounding Box:** Determine the bounding box of the non-zero pixels in the input grid.
2.  **Output Dimensions:** The output grid's width is always 6. The output grid's height is equal to the height of the input bounding box.
3.  **Iterate through Rows:** Process each row within the input bounding box, from top to bottom.
4.  **Row Transformation:** For each input row:
    *   Create a corresponding output row.
    *   Iterate through the non-zero colors in the input row.
    *   For each non-zero color, place it in the output row, followed by itself, then followed by a 0.
    *   Repeat this "color, color, 0" pattern until the output row is filled (width 6). If a color from the input is partially written to the output, continue on the next row, do not reset.
5. Since each row in the output is generated independently, using the input row to determine output colors, the last row will follow the pattern of each of the previous rows.
"""

import numpy as np

def get_bounding_box(grid):
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return rmin, rmax, cmin, cmax

def transform(input_grid):
    # convert input to numpy array
    input_grid = np.array(input_grid)

    # Find object bounding box
    rmin, rmax, cmin, cmax = get_bounding_box(input_grid)
    height = rmax - rmin + 1
    width = 6

    # Initialize output grid (height x 6)
    output_grid = np.zeros((height, width), dtype=int)

    # Row transformation
    output_row_index = 0
    for i in range(rmin, rmax + 1):
        row = input_grid[i, :]
        non_zero_colors = row[row != 0]
        color_index = 0

        while output_row_index % width < width:
            if color_index < len(non_zero_colors):
              output_grid[i-rmin, output_row_index % width] = non_zero_colors[color_index]
              output_row_index += 1
              if output_row_index % width < width:
                output_grid[i-rmin, output_row_index % width] = non_zero_colors[color_index]
                output_row_index += 1

              if output_row_index % width < width:
                output_grid[i - rmin, output_row_index % width] = 0
                output_row_index+=1

              color_index += 1

            else:
                color_index = 0

        output_row_index = 0


    return output_grid.tolist()
```