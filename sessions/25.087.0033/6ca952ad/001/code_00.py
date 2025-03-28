import numpy as np
from collections import deque

"""
Identify the background color (most frequent color).
Find all connected objects of non-background colors using 8-way connectivity.
Determine the size of each object.
Objects with size greater than 3 are considered "falling" objects.
Objects with size less than or equal to 3 are considered "stationary" objects.
Initialize the output grid with the background color.
Place the stationary objects onto the output grid in their original positions.
Sort the falling objects based on their top-most row coordinate (minimum row index), ascending.
For each falling object, simulate its fall downwards:
  Determine the maximum distance it can fall vertically until it hits the bottom boundary or another pixel already placed in the output grid (either a stationary object or a previously fallen object).
  Place the object in the output grid at its final resting position.
Return the modified output grid.
"""

def find_background(grid):
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def find_objects(grid, background_color):
    """Finds all connected objects of non-background colors."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    # Directions for 8-way connectivity (including diagonals)
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                # Start BFS for a new object
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                
                while q:
                    row, col = q.popleft()
                    color = grid[row, col]
                    obj_pixels.append({'r': row, 'c': col, 'color': color})
                    
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] != background_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({
                    'pixels': obj_pixels,
                    'size': len(obj_pixels),
                    'min_r': min_r,
                    'max_r': max_r
                })
                
    return objects

def transform(input_grid):
    """
    Applies gravity to objects larger than 3 pixels in size.
    Smaller objects remain stationary.
    """
    input_np = np.array(input_grid)
    height, width = input_np.shape
    
    # 1. Find Background Color
    background_color = find_background(input_np)
    
    # 2. Find Objects
    objects = find_objects(input_np, background_color)
    
    # 3. Initialize Output Grid
    output_grid = np.full_like(input_np, background_color)
    
    # 4. Identify Falling and Stationary Objects
    falling_objects = []
    stationary_objects = []
    for obj in objects:
        if obj['size'] > 3:
            falling_objects.append(obj)
        else:
            stationary_objects.append(obj)
            
    # 5. Place Stationary Objects
    for obj in stationary_objects:
        for pixel in obj['pixels']:
            output_grid[pixel['r'], pixel['c']] = pixel['color']
            
    # 6. Simulate Falling
    # Sort falling objects by their top-most row (min_r)
    falling_objects.sort(key=lambda obj: obj['min_r'])
    
    # Process each falling object
    for obj in falling_objects:
        obj_pixels = obj['pixels']
        current_offset_r = 0
        
        # Determine how far the object can fall
        while True:
            next_offset_r = current_offset_r + 1
            can_move = True
            # Check collision for the next potential position
            for pixel in obj_pixels:
                target_r = pixel['r'] + next_offset_r
                target_c = pixel['c']
                
                # Check bounds
                if target_r >= height:
                    can_move = False
                    break
                # Check collision with existing pixels in output_grid
                if output_grid[target_r, target_c] != background_color:
                    # Need to ensure it's not colliding with a part of itself
                    # Check if the colliding pixel belongs to the current object *at its potential new position*
                    is_self_collision = False
                    for p_self in obj_pixels:
                        if (p_self['r'] + next_offset_r == target_r and
                            p_self['c'] == target_c):
                           is_self_collision = True
                           break
                    if not is_self_collision:
                       can_move = False
                       break

            if can_move:
                current_offset_r = next_offset_r
            else:
                # Cannot move further, current_offset_r is the final offset
                break
                
        # Place the object at its final position
        for pixel in obj_pixels:
            final_r = pixel['r'] + current_offset_r
            final_c = pixel['c']
            output_grid[final_r, final_c] = pixel['color']
            
    return output_grid.tolist()