# 0a938d79 • 020 • refine_coder

---
```python
"""
1.  **Find Key Pixels:** Locate the single red (value 2) pixel and the single green (value 3) pixel within the input grid. Record their row indices.
2.  **Identify Red Chunk Extent:**
    The rows including and above the red pixel row, up to but not including the next green pixel row or the top of the grid are the "red chunk".
3. **Identify Green Chunk Extent:**
    The rows including and above the green pixel row, up to but not including the next red pixel row or the top of the grid are the "green chunk".
4.  **Expand Initial Chunks:** Fill all pixels in the rows of the initially identified "red chunk" with red (2). Fill all pixels in the rows of the initially identified "green chunk" with green (3).
5.  **Repeat Chunks:** Starting above the initial chunks, alternate filling subsequent rows with the full "red chunk", then the full "green chunk", upwards to the top of the grid.
6.  **Repeat Chunks (downward):** Starting below the initial chunks, alternate filling subsequent rows with the full "green chunk", then the full "red chunk", downwards to the bottom of the grid.
7.  **Maintain Grid Size:** The output grid has the same dimensions (width and height) as the input grid.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first pixel of a given color."""
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            if pixel == color:
                return (i, j)  # (row, col)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the red and green pixels
    red_pos = find_pixel(input_grid, 2)
    green_pos = find_pixel(input_grid, 3)

    if red_pos is None or green_pos is None:
        return output_grid

    # Identify Red and Green Chunk Extents
    red_chunk_start = red_pos[0]
    green_chunk_start = green_pos[0]

    # Determine chunk boundaries, handling cases where red is above or below green
    if red_pos[0] < green_pos[0]: # Red is above green
      red_chunk_end = 0
      for r in range(red_pos[0] - 1, -1, -1):
          if input_grid[r, :].any() == 3:
            red_chunk_end = r + 1
            break

      green_chunk_end = red_pos[0] + 1
      if green_pos[0] > red_pos[0]: # accounts for adjacent chunks
         for r in range(green_pos[0]-1, red_pos[0], -1):
            if (input_grid[r,:] == 2).any():
              green_chunk_end = r+1
              break

    else:  # Green is above red
      green_chunk_end = 0
      for r in range(green_pos[0] - 1, -1, -1):
        if input_grid[r,:].any() == 2:
          green_chunk_end = r + 1
          break

      red_chunk_end = green_pos[0] + 1
      if red_pos[0] > green_pos[0]:
        for r in range(red_pos[0]-1, green_pos[0], -1):
          if (input_grid[r,:] == 3).any():
            red_chunk_end = r+1
            break


    # Expand Initial Chunks
    output_grid[red_chunk_end:red_chunk_start + 1, :] = 2
    output_grid[green_chunk_end:green_chunk_start + 1, :] = 3

    # Repeat Chunks Upwards
    red_chunk_size = red_chunk_start - red_chunk_end + 1
    green_chunk_size = green_chunk_start - green_chunk_end + 1

    current_chunk_start = red_chunk_end - green_chunk_size
    while current_chunk_start >= 0:
        output_grid[current_chunk_start:current_chunk_start + green_chunk_size, :] = 3
        current_chunk_start -= red_chunk_size
        if current_chunk_start >=0:
            output_grid[current_chunk_start:current_chunk_start+red_chunk_size, :] = 2
            current_chunk_start -= green_chunk_size

    current_chunk_start = green_chunk_start + 1


    # correct for scenarios where red is above, and the green is next
    if red_pos[0] < green_pos[0]:
        current_chunk_start =  red_chunk_start + 1
    while current_chunk_start < output_grid.shape[0]:

      # determine next chunk, and add, switching color
      if red_pos[0] < green_pos[0]:
        output_grid[current_chunk_start:current_chunk_start + green_chunk_size, :] = 3
        current_chunk_start += green_chunk_size

        if current_chunk_start < output_grid.shape[0]:
          output_grid[current_chunk_start:current_chunk_start+red_chunk_size,:] = 2
          current_chunk_start += red_chunk_size
      else:
        output_grid[current_chunk_start:current_chunk_start + red_chunk_size, :] = 2
        current_chunk_start += red_chunk_size
        if current_chunk_start < output_grid.shape[0]:
            output_grid[current_chunk_start:current_chunk_start + green_chunk_size,:] = 3
            current_chunk_start += green_chunk_size


    return output_grid
```
