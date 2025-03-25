```python
"""
1.  **Identify Input Object:** Find the contiguous non-zero pixels in the input grid. Determine the bounding box (min/max row and min/max column) of this object.

2.  **Determine Core and Unique Colors:** Calculate the frequency of each non-zero color within the object. The core color is the most frequent color.  If there's a color that appears only once, it's the unique color. If no unique colors exist, check if there exists colors that tie in lowest frequency and pick the first one encountered as pseudo-unique color.

3.  **Locate Unique/Pseudo-Unique Pixel:** Find the coordinates of the unique color pixel. If no unique color exists, find the coordinates of pseudo-unique color pixels.

4. **Determine Output Dimensions:** Calculate the final dimensions of the output: `output_rows = object_height + 2`, `output_cols = object_width + 2`, where `object_height = max_row - min_row +1` and `object_width = max_col - min_col + 1`.

5.  **Create a 3x3 Core:** Create a 3x3 block filled with the core color.

6.  **Position and Mirror based on Unique/Pseudo-Unique Pixel:**
    *   If a unique pixel exists and is located on an edge of the object's bounding box:
        *   Right edge: Create a horizontal mirror of the 3x3 core to the *left*.
        *   Left edge: Create a horizontal mirror of the 3x3 core to the *right*.
        *   Bottom edge: Create a vertical mirror of the 3x3 core *above*.
        *   Top edge: Create a vertical mirror of the 3x3 core *below*.
    *   If a unique pixel is in a corner:
        * Mirror horizontally *and* vertically *and* diagonally to the opposite corner quadrant.
    * If there are only two pixels colors, and no true unique pixel, consider the less frequent color the "pseudo-unique" and use position of the first encountered pixel.

7.  **Construct Output Grid:** Create an output grid of zeros with the calculated dimensions. Place the 3x3 core and its mirrored versions based on the unique/pseudo-unique pixel's location.

8. Place original `core` to the center position of the `output_grid`.

"""

import numpy as np

def find_object_and_bbox(grid):
    """Finds the object (non-zero pixels) and its bounding box."""
    non_zero_pixels = np.argwhere(grid != 0)
    if len(non_zero_pixels) == 0:
        return [], None  # No object found

    min_row, min_col = np.min(non_zero_pixels, axis=0)
    max_row, max_col = np.max(non_zero_pixels, axis=0)
    object_pixels = [(r, c) for r in range(min_row, max_row + 1)
                     for c in range(min_col, max_col + 1)
                     if grid[r, c] != 0]
    bbox = ((min_row, max_row), (min_col, max_col))
    return object_pixels, bbox

def get_core_and_unique_colors(grid, object_pixels):
    """Identifies the core and unique/pseudo-unique colors within the object."""
    if not object_pixels:
        return None, None, None

    color_counts = {}
    for r, c in object_pixels:
        color = grid[r, c]
        color_counts[color] = color_counts.get(color, 0) + 1

    sorted_colors = sorted(color_counts.items(), key=lambda item: item[1], reverse=True)
    core_color = sorted_colors[0][0]
    unique_color = None
    pseudo_unique_color = None

    if len(sorted_colors) > 1:
      min_count = min(count for _, count in sorted_colors)
      min_colors = [color for color, count in sorted_colors if count == min_count]
      if len(min_colors) == 1 and min_count == 1:
        unique_color = min_colors[0]
      elif len(min_colors) >= 1:
        pseudo_unique_color = min_colors[0]
    
    return core_color, unique_color, pseudo_unique_color

def find_pixel_location(grid, object_pixels, color):
    """Finds the first location of a given color within the object."""
    if color is None:
        return None
    for r, c in object_pixels:
        if grid[r, c] == color:
            return (r, c)
    return None

def determine_output_dimensions(bbox):
    """Calculates output dimensions based on the bounding box."""
    (min_row, max_row), (min_col, max_col) = bbox
    object_height = max_row - min_row + 1
    object_width = max_col - min_col + 1
    return object_height + 2, object_width + 2

def determine_mirroring(bbox, unique_pixel_loc):
    """Determines mirroring operations based on unique pixel location."""
    if unique_pixel_loc is None:
        return False, False, False  # No mirroring

    (min_row, max_row), (min_col, max_col) = bbox
    row, col = unique_pixel_loc

    horizontal_mirror = False
    vertical_mirror = False
    diagonal_mirror = False

    # Edge mirroring
    if col == max_col:
        horizontal_mirror = True  # Right edge
    if col == min_col:
        horizontal_mirror = True  # Left edge
    if row == max_row:
        vertical_mirror = True  # Bottom edge
    if row == min_row:
        vertical_mirror = True  # Top edge

    # Corner mirroring
    if row == min_row and col == min_col:
        diagonal_mirror = True  # Top-left
    if row == min_row and col == max_col:
        diagonal_mirror = True  # Top-right
    if row == max_row and col == min_col:
        diagonal_mirror = True  # Bottom-left
    if row == max_row and col == max_col:
        diagonal_mirror = True  # Bottom-right
        
    return horizontal_mirror, vertical_mirror, diagonal_mirror

def create_and_place_core(output_grid, core_color):
  """Creates 3x3 core block"""
  core = np.full((3, 3), core_color)
  center_row = output_grid.shape[0] // 2
  center_col = output_grid.shape[1] // 2
  output_grid[center_row-1:center_row+2, center_col-1:center_col+2] = core
  return output_grid

def apply_mirroring(output_grid, core_color, horizontal_mirror, vertical_mirror, diagonal_mirror, unique_pixel_loc, bbox):
    """Applies mirroring to the output grid based on flags."""
    core = np.full((3, 3), core_color)
    center_row = output_grid.shape[0] // 2
    center_col = output_grid.shape[1] // 2
    (min_row, max_row), (min_col, max_col) = bbox

    # Horizontal mirroring
    if horizontal_mirror:
        if unique_pixel_loc[1] == max_col:  # Right
            output_grid[center_row - 1:center_row + 2, center_col - 4:center_col - 1] = np.fliplr(core)
        elif unique_pixel_loc[1] == min_col: # Left
             output_grid[center_row - 1:center_row + 2, center_col + 2:center_col + 5] = np.fliplr(core)
    # Vertical mirroring
    if vertical_mirror:
        if unique_pixel_loc[0] == max_row:  # Bottom
            output_grid[center_row - 4:center_row - 1, center_col - 1:center_col + 2] = np.flipud(core)
        elif unique_pixel_loc[0] == min_row:  #Top
            output_grid[center_row + 2:center_row + 5, center_col - 1:center_col + 2] = np.flipud(core)

    # Diagonal mirroring
    if diagonal_mirror:
       flipped = np.transpose(core)
       if unique_pixel_loc == (min_row, min_col): #top-left
            output_grid[center_row + 2:center_row + 5, center_col+2:center_col+5] = flipped
       if unique_pixel_loc == (min_row, max_col):  #top-right
            output_grid[center_row + 2:center_row + 5, center_col - 4:center_col - 1] = flipped
       if unique_pixel_loc == (max_row, min_col):  #bottom-left
            output_grid[center_row - 4:center_row - 1, center_col+2:center_col+5] = flipped
       if unique_pixel_loc == (max_row, max_col):  #bottom-right
            output_grid[center_row - 4:center_row - 1, center_col - 4:center_col - 1] = flipped
    return output_grid

def transform(input_grid):
    # Find the object and its bounding box
    object_pixels, bbox = find_object_and_bbox(input_grid)

    # Get the core and unique/pseudo colors
    core_color, unique_color, pseudo_unique_color = get_core_and_unique_colors(input_grid, object_pixels)

    # Find the location of the unique or pseudo-unique pixel
    unique_pixel_loc = find_pixel_location(input_grid, object_pixels, unique_color)
    if unique_pixel_loc is None:
        unique_pixel_loc = find_pixel_location(input_grid, object_pixels, pseudo_unique_color)

    # Determine output dimensions
    output_rows, output_cols = determine_output_dimensions(bbox)

    # Create output grid
    output_grid = np.zeros((output_rows, output_cols), dtype=int)
    
    # Determine mirroring
    horizontal_mirror, vertical_mirror, diagonal_mirror = determine_mirroring(bbox, unique_pixel_loc)

    # Create and place core
    output_grid = create_and_place_core(output_grid, core_color)

    # Apply mirroring
    output_grid = apply_mirroring(output_grid, core_color, horizontal_mirror, vertical_mirror, diagonal_mirror, unique_pixel_loc, bbox)


    return output_grid
```