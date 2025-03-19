"""
1.  **Identify the green shape:** Locate the contiguous region of pixels with the value 3 (green) within the input grid.
2.  **Fill the interior:** Starting from the pixel at coordinates (4,4) on the green object and change the color of green pixels to yellow color (4), to its adjacent green pixels until the color is applied to green pixels that do not have another adjacent green pixel, where adjacent include the 8 nearby pixels.
3. **Output modified grid** Create a copy of the original image. Fill in the defined region by changing pixel values from green color to yellow.
4.  The rest of the grid remains unchanged.
"""

import numpy as np

def get_contiguous_pixels(grid, start_pixel, color):
    """
    Finds all pixels contiguous to a starting pixel of a given color using an 8 neighbor adjacency.

    Args:
        grid: The 2D numpy array representing the grid.
        start_pixel: A tuple (row, col) representing the starting pixel.
        color: The color value to match.

    Returns:
        A set of (row, col) tuples representing the contiguous pixels of the given color.
    """

    rows, cols = grid.shape
    visited = set()
    to_visit = {start_pixel}

    while to_visit:
      current_pixel = to_visit.pop()
      visited.add(current_pixel)

      row, col = current_pixel
      for i in range(-1, 2):
        for j in range(-1, 2):
          if i == 0 and j == 0:
            continue
          new_row, new_col = row + i, col + j
          if 0 <= new_row < rows and 0 <= new_col < cols:  # Ensure within bounds
             if (new_row, new_col) not in visited and grid[new_row, new_col] == color:
               to_visit.add((new_row, new_col))

    return visited

def transform(input_grid):
    """
    Transforms the input grid by filling an internal region of the green shape with yellow.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find all pixels contiguous to a starting pixel, assumed to be of value 'green' (3).

    rows, cols = input_grid.shape
    green_pixels = []
    for r in range(rows):
      for c in range(cols):
         if input_grid[r,c] == 3:
           green_pixels.append((r,c))
    if len(green_pixels) == 0: return output_grid # if no green, do nothing

    # fill identified pixels with yellow color
    fill_start = (4,4)
    # check if starting fill pixel lies within green pixels
    if input_grid[fill_start] != 3:
      #find closest green pixel
      min_distance = float('inf')
      for pixel in green_pixels:
          distance = abs(pixel[0] - fill_start[0] ) + abs(pixel[1] - fill_start[1])
          if distance < min_distance:
            min_distance = distance
            fill_start = pixel

    pixels_to_fill = get_contiguous_pixels(input_grid, fill_start, 3) #get all connected green, start from center (4,4)

    # Fill the identified region with yellow (4)
    for row, col in pixels_to_fill:
        output_grid[row, col] = 4

    return output_grid