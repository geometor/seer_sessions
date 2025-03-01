"""
1.  **Identify the Cross:** Locate the cross-shaped object within the grid. The cross is defined by a central blue (1) pixel. The cross extends outwards, and can be of different colors and variable lengths.
2.  **Find the Center:** Determine the center of the cross by finding the coordinates of the blue (1) pixel.
3. **Determine Arm Colors and Extents**: For each direction (up, down, left, right), traverse outwards from the center pixel until a pixel of color 0 is found. Record the length and color of the arm.
4.  **Inflate Center:** Create a 3x3 block of blue (1) pixels centered on the original blue pixel.
5.  **Inflate Cross**: Create a cross-shaped structure centered on the original blue pixel.
    *   Extend each arm such that it becomes three pixels wide perpendicular to the original direction, with the original arm forming the center.
6. **Mirror**: For any arm that is not the full extent of the input, mirror the arm across the center.
"""

import numpy as np

def find_cross_center(grid):
    # Find the center of the cross shape (blue pixel)
    rows, cols = np.where(grid == 1)
    if len(rows) > 0:
        return (int(np.mean(rows)), int(np.mean(cols)))
    return None

def get_arm_extents(grid, center):
    extents = {}
    directions = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1),
    }
    
    for dir_name, (dr, dc) in directions.items():
        row, col = center
        length = 0
        pixels = []
        while True:
            row += dr
            col += dc
            if not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]):
                break  # Out of bounds
            if grid[row,col] == 0:
                break;
            length += 1
            pixels.append((row,col, grid[row,col]))

        if length>0:
            extents[dir_name] = {'length': length, 'pixels': pixels}

    return extents

def transform(input_grid):
    # Initialize output_grid with the same dimensions and background color (white)
    output_grid = np.zeros_like(input_grid)

    # Find the cross center
    center = find_cross_center(input_grid)

    if center is None:
        return output_grid  # Return empty grid if no cross is found

    # Get arm extents
    extents = get_arm_extents(input_grid, center)

    # Inflate the center (blue)
    for i in range(center[0] - 1, center[0] + 2):
        for j in range(center[1] - 1, center[1] + 2):
            if 0 <= i < output_grid.shape[0] and 0 <= j < output_grid.shape[1]:
                output_grid[i, j] = 1

    # Inflate and mirror arms
    for dir_name, arm_data in extents.items():
        for pixel_data in arm_data['pixels']:
            row,col, color = pixel_data
            
            if dir_name == 'up' or dir_name == 'down':
                for j in range(col-1, col+2):
                     if 0 <= j < output_grid.shape[1]:
                        output_grid[row,j] = color
                
            elif dir_name == 'left' or dir_name == 'right':
                for i in range(row-1, row+2):
                    if 0 <= i < output_grid.shape[0]:
                        output_grid[i,col] = color

    # Mirror arms
    for dir_name, arm_data in extents.items():
        if dir_name == 'up' and 'down' not in extents:
            for pixel_data in arm_data['pixels']:
              row, col, color = pixel_data
              mirrored_row = center[0] + (center[0]-row)
              if 0 <= mirrored_row < output_grid.shape[0]:
                  for j in range(col - 1, col + 2):
                    if 0 <= j < output_grid.shape[1]:
                        output_grid[mirrored_row,j] = color

        elif dir_name == 'down' and 'up' not in extents:
            for pixel_data in arm_data['pixels']:
              row, col, color = pixel_data
              mirrored_row = center[0] + (center[0]-row)
              if 0 <= mirrored_row < output_grid.shape[0]:
                  for j in range(col - 1, col + 2):
                    if 0 <= j < output_grid.shape[1]:
                        output_grid[mirrored_row,j] = color

        elif dir_name == 'left' and 'right' not in extents:
            for pixel_data in arm_data['pixels']:
              row, col, color = pixel_data
              mirrored_col = center[1] + (center[1] - col)
              if 0<= mirrored_col < output_grid.shape[1]:
                  for i in range(row - 1, row + 2):
                        if 0 <= i < output_grid.shape[0]:
                            output_grid[i,mirrored_col] = color

        elif dir_name == 'right' and 'left' not in extents:
          for pixel_data in arm_data['pixels']:
              row, col, color = pixel_data
              mirrored_col = center[1] + (center[1] - col)
              if 0<= mirrored_col < output_grid.shape[1]:
                for i in range(row - 1, row + 2):
                    if 0 <= i < output_grid.shape[0]:
                        output_grid[i,mirrored_col] = color

    return output_grid