# fcb5c309 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Green Pixels:** Locate all pixels in the input grid with the value '3' (green).
2.  **Determine Boundary:** Find the bounding box, or outline, around *all* the green pixels in the input grid. The green pixels don't need to be contiguous, but they define the external shape.
3. **Create Output:** Create output grid from identified boundary.
4. **Fill Outline:** Set all pixels within and on the outline to the color green (3).
5. **Fill Inside** Set all pixels within the outline, to the color white (0)
"""

import numpy as np

def get_green_pixel_coords(grid):
    # Find coordinates of all green pixels (value 3).
    return np.argwhere(grid == 3)

def get_bounding_box(coords):
    # Calculate the bounding box of a set of coordinates.
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find coordinates of all green pixels.
    green_coords = get_green_pixel_coords(np.array(input_grid))

    # Determine the bounding box around the green pixels.
    min_row, max_row, min_col, max_col = get_bounding_box(green_coords)
    
    # Create output grid from identified boundary.
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # create grid of all green within bounding box
    for r in range(output_height):
       for c in range(output_width):
          output_grid[r,c] = 3

    # determine interior
    # get the coordinates of green pixels in input_grid relative to bounding box
    rel_green_coords = green_coords - [min_row,min_col]
    
    # Create a mask for the "inside" based on original green pixel locations.
    inside_mask = np.zeros((output_height, output_width), dtype=bool)
    for r, c in rel_green_coords:
        inside_mask[r,c] = True

    # use a simple fill - for points not in original green, count neighbors
    # any point not a green point, but adjacent to 2 or more green points, is in the inside
    # we assume non-green areas surrounded by green are interior
    for r in range(output_height):
      for c in range(output_width):
         if not inside_mask[r,c]:
            neighbor_count = 0
            if r > 0 and output_grid[r-1,c] == 3:
               neighbor_count += 1
            if r < output_height - 1 and output_grid[r+1, c] == 3:
               neighbor_count += 1
            if c > 0 and output_grid[r,c-1] == 3:
               neighbor_count += 1
            if c < output_width - 1 and output_grid[r,c+1] == 3:
               neighbor_count += 1
            if neighbor_count >= 2:
               inside_mask[r,c] = True

    # Apply the mask and color the inside white.
    for r in range(output_height):
      for c in range(output_width):
        if inside_mask[r,c] == True:
            if output_grid[r,c] != 3:
                output_grid[r,c] = 0

    return output_grid.tolist()
```
