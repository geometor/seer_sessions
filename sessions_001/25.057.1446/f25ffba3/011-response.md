# f25ffba3 • 011 • refine_coder

---
```python
"""
1.  **Identify the Red Line:** Find the rightmost vertical line of red pixels in both the input and output grids.
2.  **Identify the Finger:** Find the "finger" of contiguous non-zero, non-red pixels connected to the red line in both the input and the output. The finger can extend in any of the four cardinal directions (up, down, left, or right) from the red line.
3.  **Finger directions.** Consider all four directions from both the top and the bottom of the red line.
4.  **Calculate Finger Translation:** Determine the row and column offset between the starting pixel (attachment to red line) of the finger in the input and output grids.  This represents how the entire finger has moved.
5.  **Calculate Red Line Translation:** Determine the column offset between the red line in the input and output grid.
6.  **Apply Translation:**
    *   Move the finger in the input grid by the calculated row and column offset.
    *   Move the red line by the calculated column offset.
7.  **Output:** The transformed grid consists of the translated finger and red line; all other pixels are black (0).
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find the rightmost column where all elements match color
    for j in range(grid.shape[1] - 1, -1, -1):
        if np.all(grid[:, j] == color):
            return j
    return -1

def find_fingers(grid, line_col, line_color):
    #find all fingers connected to a vertical line
    fingers = []

    if line_col == -1:
        return fingers # No line, so no fingers

    # Find the row where the vertical line starts and ends
    start_row = 0
    for row in range(grid.shape[0]):
        if grid[row, line_col] == line_color:
            start_row = row
            break

    end_row = grid.shape[0] -1
    for row in range(grid.shape[0] - 1, -1, -1):
        if grid[row, line_col] == line_color:
            end_row = row
            break

    # Check above
    finger = []
    for row in range(start_row - 1, -1, -1):
        if grid[row, line_col] != 0 and grid[row, line_col] != line_color:
            finger.append((row, line_col, grid[row, line_col]))
        else:
            break
    if finger:
        fingers.append(finger)

    # Check below
    finger = []
    for row in range(end_row + 1, grid.shape[0]):
        if grid[row, line_col] != 0 and grid[row, line_col] != line_color:
            finger.append((row, line_col, grid[row, line_col]))
        else:
            break
    if finger:
        fingers.append(finger)

    # Scan to the left from line end point
    finger = []
    for j in range(line_col - 1, -1, -1):
        if grid[end_row, j] != 0 and grid[end_row, j] != line_color:
            finger.append((end_row, j, grid[end_row, j]))
        else:
            break
    if finger:
        fingers.append(finger[::-1])  # Correct the reversing

    # Scan to the left from line start point
    finger = []
    for j in range(line_col - 1, -1, -1):
        if grid[start_row, j] != 0 and grid[start_row, j] != line_color :
            finger.append((start_row, j, grid[start_row, j]))
        else:
            break
    if finger:
        fingers.append(finger[::-1])  # Correct the reversing

    #scan to the right from the line start point
    finger = []
    for j in range(line_col + 1, grid.shape[1]):
      if grid[start_row, j] != 0 and grid[start_row,j] != line_color:
        finger.append( (start_row, j, grid[start_row,j]))
      else:
        break;
    if finger:
      fingers.append(finger)

    #scan to the right from the line end point
    finger = []
    for j in range(line_col + 1, grid.shape[1]):
      if grid[end_row, j] != 0 and grid[end_row,j] != line_color:
        finger.append( (end_row, j, grid[end_row,j]))
      else:
        break;
    if finger:
      fingers.append(finger)

    return fingers

def calculate_translation(input_finger, output_finger):
    #determine row/col offset, assuming input and output are same length
    if not input_finger or not output_finger:
        return 0, 0
    input_start = input_finger[0]
    output_start = output_finger[0]
    row_offset = output_start[0] - input_start[0]
    col_offset = output_start[1] - input_start[1]
    return row_offset, col_offset

def translate_finger(grid, finger, row_offset, col_offset):
    # Move a finger by row and column offset
    for i, j, color in finger:
        new_row = i + row_offset
        new_col = j + col_offset
        if 0 <= new_row < grid.shape[0] and 0 <= new_col < grid.shape[1]:
            grid[new_row, new_col] = color

def translate_line(grid, line_col, color, col_offset):
  #move a vertical line by a col offset
  if line_col == -1:
    return
  
  new_col = line_col + col_offset
  if new_col < 0 or new_col >= grid.shape[1]:
    return;

  for row in range(grid.shape[0]):
    if grid[row, line_col] == color:
      grid[row, new_col] = color

def transform(input_grid):
    # 1. Identify the Red Line
    input_red_line_col = find_vertical_line(input_grid, 2)

    # 2. Identify the Fingers
    input_fingers = find_fingers(input_grid, input_red_line_col, 2)
    # Create a blank output grid (all black)
    output_grid = np.zeros_like(input_grid)

    #find the red line and finger in the output_grid by inverting the input
    output_red_line_col = find_vertical_line(input_grid[::-1, ::-1], 2)
    output_fingers = find_fingers(input_grid[::-1, ::-1], output_red_line_col, 2)

    red_line_col_offset = 0
    if input_red_line_col != -1 and output_red_line_col != -1:
      red_line_col_offset =  (input_grid.shape[1] -1 - output_red_line_col) - input_red_line_col

    # 3. & 4. Calculate Finger Translation
    row_offset, col_offset = 0, 0
    if input_fingers and output_fingers:
        row_offset, col_offset = calculate_translation(input_fingers[0], output_fingers[0])

    # 5. & 6. Apply Translation to finger and red line
    if input_fingers:
        for finger in input_fingers:
          translate_finger(output_grid, finger, row_offset, col_offset)

    translate_line(output_grid, input_red_line_col, 2, red_line_col_offset)


    return output_grid
```
