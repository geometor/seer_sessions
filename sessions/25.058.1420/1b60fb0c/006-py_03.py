"""
Finds regions of white pixels (0) fully enclosed by blue pixels (1) and changes the white pixels to red (2).
"""

import numpy as np

def find_blue_objects(grid):
    # Find the coordinates of all blue (1) pixels.
    blue_pixels = np.argwhere(grid == 1)
    return blue_pixels

def find_enclosed_area(grid, blue_pixels):
    enclosed_areas = []

    if len(blue_pixels) == 0:
        return enclosed_areas

    # Create a set of blue pixel coordinates for efficient lookup.
    blue_pixels_set = set(map(tuple, blue_pixels))

    # Iterate through all pixels in the grid.
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            # Only check for white pixels (0).
            if grid[r, c] == 0:
                # Check if the current pixel is part of an enclosed area.
                neighbors = []
                if r > 0:
                    neighbors.append((r - 1, c))
                if r < grid.shape[0] - 1:
                    neighbors.append((r + 1, c))
                if c > 0:
                    neighbors.append((r, c - 1))
                if c < grid.shape[1] - 1:
                    neighbors.append((r, c + 1))

                # Check all neighbors and see if the are all either 0 or blue.
                all_neighbors_blue_or_zero = True
                for nr, nc in neighbors:
                    if (nr, nc) not in blue_pixels_set and grid[nr, nc] != 0:
                      all_neighbors_blue_or_zero = False
                      break
                
                if all_neighbors_blue_or_zero:
                    
                  # Use a flood fill algorithm to determine fully enclosed zero region
                  visited = set()
                  queue = [(r, c)]
                  enclosed = True
                  current_area = []

                  while queue:
                    curr_r, curr_c = queue.pop(0)
                    
                    if (curr_r, curr_c) in visited:
                      continue

                    visited.add((curr_r, curr_c))
                    current_area.append((curr_r, curr_c))


                    # Get neighbors
                    neighbors = []
                    if curr_r > 0:
                        neighbors.append((curr_r - 1, curr_c))
                    if curr_r < grid.shape[0] - 1:
                        neighbors.append((curr_r + 1, curr_c))
                    if curr_c > 0:
                        neighbors.append((curr_r, curr_c - 1))
                    if curr_c < grid.shape[1] - 1:
                        neighbors.append((curr_r, curr_c + 1))

                    for nr, nc in neighbors:
                        if (nr, nc) not in visited:
                            if grid[nr, nc] == 0:
                                queue.append((nr, nc)) #continue flood fill
                            elif (nr, nc) not in blue_pixels_set:
                                enclosed = False #not enclosed if not 0 and not blue

                  if enclosed:
                    enclosed_areas.extend(current_area)                  

    return enclosed_areas

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the blue object's pixels.
    blue_pixels = find_blue_objects(output_grid)

    # Find the enclosed area(s).
    enclosed_areas = find_enclosed_area(output_grid, blue_pixels)

    # Fill in enclosed area(s).
    for r, c in enclosed_areas:
        output_grid[r, c] = 2

    return output_grid