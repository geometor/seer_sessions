```python
"""
1.  **Identify the Rectangle and Border:** In the input grid, locate the rectangular block of a single color in the top-left corner. Identify its bordering color to the right and below. The height of the block should always be one less that the width.
2.  **Repeat Input Pattern:** Copy the original input grid twice horizontally to form the top-left 5x10 section of a new 10x10 grid.
3.  **Extend inner rectangle:** Copy only the rectangle without the border to form a rectangle one row and one column smaller than the output, so, in this case, 9x9
4.  **Fill the border**: Fill the remaining cells with the bordering colour to make a complete 10x10 output
"""

import numpy as np

def find_rectangle(grid):
    # Find the top-left corner color.
    top_left_color = grid[0, 0]
    if top_left_color == 0:
        return None, None, None, None # No rectangle found

    # Find width and height of the rectangle.
    height = 0
    for i in range(grid.shape[0]):
        if grid[i, 0] == top_left_color:
            height += 1
        else:
            break

    width = 0
    for j in range(grid.shape[1]):
        if grid[0, j] == top_left_color:
            width += 1
        else:
            break

    # Find the border color

    border_color = grid[0, width] if width < grid.shape[1] else grid[height,0]

    return 0, 0, width, height, border_color


def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the rectangle and its border color.
    rect_row, rect_col, rect_width, rect_height, border_color = find_rectangle(input_grid)

    # Initialize the output grid (10x10).
    output_grid = np.zeros((10, 10), dtype=int)
    
    # 2. repeat input
    input_height, input_width = input_grid.shape
    output_grid[:input_height, :input_width] = input_grid
    output_grid[:input_height, input_width:input_width*2] = input_grid

    # 3. extend the rectangle
    rect_color = input_grid[0,0]
    output_grid[:9, :9] = rect_color

    # 4. fill the remaining
    output_grid[:9, 9] = border_color
    output_grid[9, :10] = border_color

    return output_grid.tolist()
```