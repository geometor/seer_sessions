"""
1.  **Identify the vertical red line:** Find the vertical red line (pixels of color 2) located at the rightmost edge of the grid. This line's horizontal position does not change.

2.  **Identify the "finger":** Locate a sequence of contiguous, non-white pixels connected to the vertical red line. The finger can extend horizontally or vertically from any point along the red line.

3. **Determine Finger position:** The sequence starts at the red line. Note the colors and position of each pixel in the sequence relative to the starting pixel at the red line.

4.  **Reposition the "finger":**
    *   The "finger" sequence is copied.
    *   The copy is placed with its starting pixel at the row above where the vertical red line starts.
    *  The finger pixels are arranged along the same column as the red line, with the same relative row offsets from the finger's new start position.

5.  **Preserve other pixels:** All other pixels (which are white in the examples) remain in their original positions.

6.  **Construct the output grid:** Combine the unchanged vertical red line, the repositioned "finger," and the unchanged other pixels.
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find the rightmost column
    for j in range(grid.shape[1] - 1, -1, -1):
        # Check if the entire column is of the specified color
        if np.all(grid[:, j] == color):
            return j
    return -1  # Not found

def find_finger(grid, line_col, line_color):
    #find the row where line starts
    for start_row in range(grid.shape[0]):
      if grid[start_row, line_col] == line_color:
        break;

    # Find the row where the vertical line ends
    for end_row in range(grid.shape[0] - 1, -1, -1):
        if grid[end_row, line_col] == line_color:
            break
    else:
      return [] #no line found

    #check above
    finger = []
    if start_row > 0:
      for row in range(start_row -1, -1, -1):
        if grid[row, line_col] != 0:
          finger.append( (row, line_col, grid[row, line_col]) )
        else:
          break
    if finger:
      return finger

    #check below
    finger = []
    if end_row < grid.shape[0]-1:
      for row in range(end_row + 1, grid.shape[0]):
        if grid[row, line_col] != 0:
          finger.append( (row, line_col, grid[row, line_col]) )
        else:
          break

    if finger:
      return finger

    # Scan to the left from line end point
    finger = []
    for j in range(line_col, -1, -1):
        if grid[end_row,j] != 0:
          finger.append( (end_row, j, grid[end_row, j]) )
        else:
            break
    if finger:
        return finger[::-1]  #correct the reversing

    #scan to the left from line start point
    finger = []
    for j in range(line_col, -1, -1):
        if grid[start_row,j] != 0:
          finger.append( (start_row, j, grid[start_row, j]) )
        else:
            break
    if finger:
       return finger[::-1]  #correct the reversing

    return []

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = input_grid.copy()

    # Find the vertical red line
    red_line_col = find_vertical_line(input_grid, 2)

    if red_line_col == -1:
        return output_grid  # No red line found, return original grid

    #find start row of red line
    for start_row in range(input_grid.shape[0]):
      if input_grid[start_row, red_line_col] == 2:
        break;
    
    # Find the horizontal finger
    finger = find_finger(input_grid, red_line_col, 2)
    
    if not finger:
        return output_grid  # Return original if finger is empty

    # Calculate the relative positions of the finger pixels
    finger_relative_positions = [(row - finger[0][0], col - finger[0][1], color) for row, col, color in finger]


    # Determine the new starting position for the finger
    new_start_row = start_row - 1
    new_start_col = red_line_col

    #erase original position
    for row, col, _ in finger:
        output_grid[row, col] = 0    

    # Reposition the finger in the output grid
    for row_offset, col_offset, color in finger_relative_positions:
      new_row = new_start_row + row_offset
      new_col = new_start_col + col_offset #should always be 0

      #check bounds
      if 0 <= new_row < output_grid.shape[0]:
          output_grid[new_row, new_col] = color


    return output_grid