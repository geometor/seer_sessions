"""
The transformation rule is as follows:
1. Identify the connected component of red (2) pixels and all gray (5) pixels within the input grid. Consider white pixels as the background.
2. Move each gray (5) pixel:
   - Find locations outside of the red object that are closest to the edge of the red object.
   - Only consider corner positions within the overall grid.
   - Move the gray pixels to these new locations.
3. Keep the red object in the same position.
"""

import numpy as np

def find_objects(grid, color):
    """Finds objects of a specific color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find red object and gray pixels
    red_objects = find_objects(input_grid, 2)
    gray_pixels = find_objects(input_grid, 5)
    
    # Flatten the list of gray pixels
    gray_pixels_flat = [pixel for sublist in gray_pixels for pixel in sublist]

    # Clear original gray pixel positions in the output grid
    for r, c in gray_pixels_flat:
        output_grid[r, c] = 0

    # Determine new positions for gray pixels.
    for r_gray,c_gray in gray_pixels_flat:
        # calculate new position for gray pixel at corner of red object.
        min_dist = float('inf')
        new_pos = None

        for r_red, c_red in red_objects[0]: # assume only have one object
            # find 4 corner direction
            if (r_red,c_red-1) not in red_objects[0] and (r_red-1,c_red-1) not in red_objects[0] and (r_red-1,c_red) not in red_objects[0]:
                dist = abs(r_red - r_gray) + abs(c_red -1 - c_gray) # calculate corner position
                if dist < min_dist:
                    min_dist = dist
                    new_pos = (r_red, c_red - 1)

            if (r_red,c_red+1) not in red_objects[0] and (r_red-1,c_red+1) not in red_objects[0] and (r_red-1,c_red) not in red_objects[0]:
                dist = abs(r_red - r_gray) + abs(c_red + 1 - c_gray)
                if dist < min_dist:
                    min_dist = dist
                    new_pos = (r_red, c_red + 1)

            if (r_red+1,c_red) not in red_objects[0] and (r_red+1,c_red-1) not in red_objects[0] and (r_red,c_red-1) not in red_objects[0]:
                dist = abs(r_red+1 - r_gray) + abs(c_red - c_gray)
                if dist < min_dist:
                    min_dist = dist
                    new_pos = (r_red+1,c_red)

            if (r_red+1,c_red) not in red_objects[0] and (r_red+1,c_red+1) not in red_objects[0] and (r_red,c_red+1) not in red_objects[0]:
                dist = abs(r_red+1 - r_gray) + abs(c_red - c_gray)
                if dist < min_dist:
                    min_dist = dist
                    new_pos = (r_red+1, c_red)


        # set boundary
        if new_pos:
            r,c = new_pos
            if r < 0:
                r = 0
            if r >= output_grid.shape[0]:
                r = output_grid.shape[0]-1
            if c < 0:
                c = 0
            if c >= output_grid.shape[1]:
                c = output_grid.shape[1] - 1

            output_grid[r,c] = 5

    return output_grid