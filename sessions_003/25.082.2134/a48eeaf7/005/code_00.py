"""
Gray pixels move to be adjacent to the closest red pixel, prioritizing creating a vertical stack above the red pixels. If there are no red pixels, gray pixels remain unchanged. Gray pixels form a block and maintain their relative positions if possible, moving as a unit.
"""

import numpy as np

def find_objects(grid, color):
    """Finds the positions of all pixels of a given color."""
    return np.argwhere(grid == color)

def calculate_centroid(positions):
    """Calculates the centroid of a set of positions."""
    return np.mean(positions, axis=0) if len(positions) > 0 else None

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    
    output_grid = np.copy(input_grid)
    
    gray_positions = find_objects(input_grid, 5)
    red_positions = find_objects(input_grid, 2)

    if len(red_positions) == 0:
        return output_grid

    # Treat gray pixels as a single object (or potentially multiple)
    if len(gray_positions) > 0:
        # Calculate the centroid of the gray pixels
        gray_centroid = calculate_centroid(gray_positions)

        #find closest red position to centroid
        min_dist = float('inf')
        nearest_red_centroid = None
        for red_pos in red_positions:
            dist = abs(red_pos[0] - gray_centroid[0]) + abs(red_pos[1] - gray_centroid[1])  # Manhattan
            if dist < min_dist:
                min_dist = dist
                nearest_red_centroid = red_pos

        # Determine target position based on gray and nearest red centroids
        target_row = nearest_red_centroid[0] - 1
        target_col = nearest_red_centroid[1]

        # Move all gray pixels as a block, maintaining relative positions
        row_offset = target_row - gray_centroid[0]
        col_offset = target_col - gray_centroid[1]

        # Create new gray positions and clear old
        new_gray_positions = []
        for gray_pos in gray_positions:
            output_grid[gray_pos[0], gray_pos[1]] = 0 #clear old position

        for gray_pos in gray_positions:
            new_row = int(round(gray_pos[0] + row_offset))
            new_col = int(round(gray_pos[1] + col_offset))

            #Basic boundary check
            if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
              #if new position is red, adjust
              if output_grid[new_row, new_col] == 2:
                new_gray_positions.append((new_row, new_col+1))

              else:
                new_gray_positions.append((new_row, new_col))
            else: #pixel is out of bounds, leave in old spot.
                new_gray_positions.append((gray_pos[0], gray_pos[1]))
                output_grid[gray_pos[0], gray_pos[1]] = 5 #reset old since it didn't move

        # Check for collisions and apply additional rules
        for new_pos in new_gray_positions:
              row, col = new_pos

              if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
                output_grid[row,col] = 5
              # else, skip - pixel will remain in old place.

    return output_grid