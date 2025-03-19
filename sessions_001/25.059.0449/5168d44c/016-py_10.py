"""
1.  **Identify Objects:** Find the vertical green line and the red cross-shaped object.
2.  **Rotate Red Cross** Rotate the Red cross by 180 degrees around its center point.
3.  **Copy Green line:** Copy the green line segments below other objects.
4.  **Combine**: combine the altered green segments and the rotated red object into an output grid, maintaining relative positions, filling remaining space with white.
"""

import numpy as np

def find_object(grid, color, shape_type=None):
    objects = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append([r, c])
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                if shape_type == 'line':
                    # Check if it forms a line (vertical or horizontal)
                   if all(x[0] == current_object[0][0] for x in current_object) or all(x[1] == current_object[0][1] for x in current_object):
                        objects.append(current_object)

                elif shape_type == 'cross':
                    # Basic cross shape check (can be refined)
                    if len(current_object) > 1:
                        objects.append(current_object)

                elif shape_type is None:

                    objects.append(current_object)


    return objects


def rotate_object(object_coords, center, degrees):
    """Rotates object coordinates around a center point."""
    rotated_coords = []
    rads = np.radians(degrees)
    for r, c in object_coords:
        # Translate to origin
        r -= center[0]
        c -= center[1]
        # Rotate
        new_r = r * np.cos(rads) - c * np.sin(rads)
        new_c = r * np.sin(rads) + c * np.cos(rads)
        # Translate back
        rotated_coords.append([int(round(new_r + center[0])), int(round(new_c + center[1]))])
    return rotated_coords


def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = np.zeros_like(grid)

    # Find the green line and red cross
    green_line = find_object(grid, 3, 'line')
    red_cross = find_object(grid, 2, 'cross')
    #print(f'{green_line=}')
    #print(f'{red_cross=}')
    if not green_line or not red_cross:
       return output_grid.tolist()
    
    green_line = green_line[0]
    red_cross = red_cross[0]

    # Find center of the red_cross
    red_cross_center = [int(np.mean([x[0] for x in red_cross])), int(np.mean([x[1] for x in red_cross]))]


    # Rotate the red cross
    rotated_red_cross = rotate_object(red_cross, red_cross_center, 180)
    #print(f'{rotated_red_cross=}')

    # Find position to copy green line to
    max_row = 0
    for coord in rotated_red_cross:
        if coord[0] > max_row:
           max_row = coord[0]
    new_green_line = []

    for i in range(len(green_line)):
       new_green_line.append([max_row-len(green_line)+1 + i, green_line[0][1]])

    # Fill output grid
    for r, c in rotated_red_cross:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
            output_grid[r, c] = 2

    for r, c in new_green_line:
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
        output_grid[r, c] = 3

    return output_grid.tolist()