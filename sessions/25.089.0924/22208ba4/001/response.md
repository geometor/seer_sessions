```python
import numpy as np
from collections import Counter

"""
Identifies non-background colored objects touching the border of the input grid.
Counts the number of border objects for each color.
Determines the 'moving color' as the one with the highest count of border objects.
Initializes an output grid with the background color.
Redraws stationary objects (non-border objects OR border objects of non-moving colors) in their original positions.
Redraws moving objects (border objects of the 'moving color') shifted one step diagonally inwards towards the center.
"""

# Helper function to find connected components (objects) using Breadth-First Search
def find_objects(grid, colors_to_find=None):
    """
    Finds connected components (objects) of specified colors in the grid using 4-way connectivity.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set, optional): A set of colors to find objects for. 
                                         If None, finds objects of all colors. Defaults to None.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'coords' (set of (row, col) tuples).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    target_colors = set(colors_to_find) if colors_to_find is not None else None

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Skip visited cells, background cells (if implicitly defined by target_colors), 
            # or colors not specifically targeted
            if visited[r, c] or (target_colors is not None and color not in target_colors):
                continue
            
            # Check if this color should be part of an object
            # If target_colors is defined, it must be in the set.
            # If target_colors is None, we find objects of *any* color (usually we pre-filter).
            # In this task's context, we call this with non_background_colors, so this check is sufficient.

            # Start BFS for a new object
            q = [(r, c)]
            visited[r, c] = True
            current_object_coords = set([(r, c)])
            
            queue_idx = 0
            while queue_idx < len(q):
                row, col = q[queue_idx]
                queue_idx += 1
                
                # Check 4 neighbors (up, down, left, right)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    # Check bounds and if neighbor is same color and not visited
                    if 0 <= nr < height and 0 <= nc < width and \
                       not visited[nr, nc] and grid[nr, nc] == color:
                        visited[nr, nc] = True
                        q.append((nr, nc))
                        current_object_coords.add((nr, nc))
            
            # Add the found object if it consists of at least one pixel
            if current_object_coords:
                 objects.append({'color': color, 'coords': current_object_coords})

    return objects

# Helper function to check if an object touches the border
def is_border_object(obj_coords, grid_shape):
    """
    Checks if any coordinate of the object touches the grid border.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object's pixels.
        grid_shape (tuple): A tuple (height, width) of the grid.

    Returns:
        bool: True if the object touches the border, False otherwise.
    """
    height, width = grid_shape
    for r, c in obj_coords:
        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
            return True
    return False

# Helper function to determine the corner an object primarily occupies
def get_object_corner(obj_coords, grid_shape):
    """
    Determines the corner an object is closest to based on its coordinates.
    Uses the location of the majority of its bounding box relative to the center.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object's pixels.
        grid_shape (tuple): A tuple (height, width) of the grid.

    Returns:
        str: One of 'top-left', 'top-right', 'bottom-left', 'bottom-right'.
    """
    height, width = grid_shape
    center_r, center_c = (height - 1) / 2.0, (width - 1) / 2.0
    
    # Calculate bounding box
    min_r = min(r for r, c in obj_coords)
    max_r = max(r for r, c in obj_coords)
    min_c = min(c for r, c in obj_coords)
    max_c = max(c for r, c in obj_coords)

    # Determine vertical position based on bounding box center
    bbox_center_r = (min_r + max_r) / 2.0
    is_top = bbox_center_r < center_r

    # Determine horizontal position based on bounding box center
    bbox_center_c = (min_c + max_c) / 2.0
    is_left = bbox_center_c < center_c
    
    if is_top and is_left:
        return 'top-left'
    elif is_top and not is_left:
        return 'top-right'
    elif not is_top and is_left:
        return 'bottom-left'
    else: # not is_top and not is_left
        return 'bottom-right'

# Helper function to find the background color (most frequent color)
def find_background_color(grid):
    """
    Finds the most frequent color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The color value that appears most often. Defaults to 0 if grid is empty.
    """
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default background for an empty grid
    # Find the color with the highest count
    background_color = counts.most_common(1)[0][0]
    return background_color

def transform(input_grid):
    """
    Transforms the input grid according to the task rules:
    Identifies border objects, determines the color with the most border objects ('moving_color'),
    and moves objects of that color one step diagonally inwards, leaving others stationary.
    """
    
    input_grid_np = np.array(input_grid, dtype=int)
    if input_grid_np.size == 0:
        return [] # Handle empty input grid
        
    height, width = input_grid_np.shape
    grid_shape = (height, width)

    # 1. Determine background color
    background_color = find_background_color(input_grid_np)

    # 2. Find all non-background colors present in the grid
    unique_colors = np.unique(input_grid_np)
    non_background_colors = {c for c in unique_colors if c != background_color}

    # If there are no non-background colors, return the input grid (or a copy)
    if not non_background_colors:
        return input_grid # Or input_grid_np.tolist() if a copy is desired

    # 3. Find all objects composed of non-background colors
    all_objects = find_objects(input_grid_np, non_background_colors)

    # 4. Identify border objects and count them by color
    border_objects = []
    border_object_color_counts = Counter()
    for obj in all_objects:
        # Ensure the object color is actually non-background before checking border status
        # (find_objects should only return these based on non_background_colors filter, but double-check)
        if obj['color'] in non_background_colors and is_border_object(obj['coords'], grid_shape):
            border_objects.append(obj)
            border_object_color_counts[obj['color']] += 1

    # 5. Determine the moving color (color with the most border objects)
    moving_color = -1 # Use -1 to indicate no moving color found yet
    max_count = 0
    if border_object_color_counts:
         # Find the maximum count
         max_count = border_object_color_counts.most_common(1)[0][1]
         # Find all colors that have this maximum count
         colors_with_max_count = [color for color, count in border_object_color_counts.items() if count == max_count]
         
         # If there's at least one color with the max count, choose one.
         # Simple tie-breaking: choose the numerically smallest color value among the winners.
         if colors_with_max_count:
             moving_color = min(colors_with_max_count) 
        
    # 6. Initialize output grid filled entirely with the background color
    output_grid = np.full_like(input_grid_np, background_color)

    # 7. Process all found non-background objects
    for obj in all_objects:
        obj_color = obj['color']
        obj_coords = obj['coords']
        
        # Determine if this object should move: must be a border object AND its color must be the moving color
        is_border = is_border_object(obj_coords, grid_shape) # Re-check needed if we didn't store this earlier
        is_moving = is_border and (obj_color == moving_color)

        if is_moving:
            # This object moves diagonally inwards.
            # Determine corner to know the direction of movement.
            corner = get_object_corner(obj_coords, grid_shape)
            dr, dc = 0, 0 # delta row, delta column for movement
            if corner == 'top-left':
                dr, dc = 1, 1       # Move down-right
            elif corner == 'top-right':
                dr, dc = 1, -1      # Move down-left
            elif corner == 'bottom-left':
                dr, dc = -1, 1      # Move up-right
            elif corner == 'bottom-right':
                dr, dc = -1, -1     # Move up-left
            
            # Apply shift to each pixel of the object and draw in the output grid
            for r, c in obj_coords:
                nr, nc = r + dr, c + dc
                # Draw the pixel at the new location, checking grid bounds
                if 0 <= nr < height and 0 <= nc < width:
                    output_grid[nr, nc] = obj_color
                # Pixels moving off-grid are simply lost

        else: 
            # This object is stationary (either not a border object, or not the moving color).
            # Draw it at its original position in the output grid.
            for r, c in obj_coords:
                 # Check bounds (mostly for safety, should always be within bounds here)
                 if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = obj_color

    # 8. Convert the final numpy grid back to a list of lists
    return output_grid.tolist()
```