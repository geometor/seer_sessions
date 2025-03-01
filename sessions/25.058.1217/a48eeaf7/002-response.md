# a48eeaf7 • 002 • example_2 • investigate_coder

---
```python
"""
The transformation involves rearranging the gray pixels to cluster around the stationary red square, where the gray pixels form one shape, collecting adjacent to one another, including adjacency to the red square.
"""

import numpy as np

def find_red_square(grid):
    # Find the top-left corner of the 2x2 red square.
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            if (grid[r, c] == 2 and grid[r + 1, c] == 2 and
                grid[r, c + 1] == 2 and grid[r + 1, c + 1] == 2):
                return (r, c)
    return None

def find_gray_pixels(grid):
    # Find the coordinates of all gray pixels.
    gray_coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 5:
                gray_coords.append((r, c))
    return gray_coords

def is_adjacent(coord1, coord2):
    # Check if two coordinates are adjacent (not diagonally).
    r1, c1 = coord1
    r2, c2 = coord2
    return (abs(r1 - r2) <= 1 and c1 == c2) or (abs(c1 - c2) <= 1 and r1 == r2)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the red square.
    red_square_coords = find_red_square(input_grid)

    # Find gray pixels.
    gray_pixel_coords = find_gray_pixels(input_grid)

    # Clear the original gray pixels from the output grid.
    for r, c in gray_pixel_coords:
        output_grid[r, c] = 0
        
    # Determine target locations for gray pixels.
    target_coords = []
    if red_square_coords:
      red_r, red_c = red_square_coords
      # Add cells around red square.
      potential_targets = [
          (red_r - 1, red_c), (red_r - 1, red_c + 1), (red_r - 1, red_c + 2),
          (red_r, red_c - 1),                     (red_r, red_c + 2),
          (red_r + 1, red_c - 1),                   (red_r + 1, red_c + 2),
          (red_r + 2, red_c - 1),                     (red_r + 2, red_c + 2),
           (red_r + 2, red_c), (red_r + 2, red_c + 1)
      ]
      
      # Filter to remove coordinates off grid
      valid_targets = [(r,c) for r, c in potential_targets if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]]

      placed_gray_pixels = []

      # Try to arrange according to adjacency
      for gray_pixel in gray_pixel_coords:
          found_spot = False
          for target in valid_targets:
              # Check if the target is empty
              if output_grid[target] == 0:
                  # check for adjacency to red square or existing gray pixel
                  adjacent_to_placed = False
                  if len(placed_gray_pixels) > 0:
                      for placed in placed_gray_pixels:
                          if is_adjacent(target, placed):
                              adjacent_to_placed = True
                              break
                  
                  if is_adjacent(target, (red_r,red_c)) or is_adjacent(target, (red_r+1,red_c)) or is_adjacent(target, (red_r,red_c+1)) or is_adjacent(target, (red_r+1,red_c+1)) or adjacent_to_placed:
                      output_grid[target] = 5
                      placed_gray_pixels.append(target)
                      valid_targets.remove(target)
                      found_spot = True
                      break # move on to next gray
          if not found_spot:
            # we should attempt to put it next to any of the gray pixels that have already been placed
            # first get placed locations
            for target in valid_targets:
                if output_grid[target] == 0:
                    for placed in placed_gray_pixels:
                        if is_adjacent(target, placed):
                            output_grid[target] = 5
                            placed_gray_pixels.append(target)
                            valid_targets.remove(target)
                            found_spot = True
                            break
                if found_spot:
                    break



    return output_grid
```
