```python
import numpy as np
from collections import Counter

"""
Selectively move border objects towards the center based on color frequency at the borders.
The transformation identifies the background color (most frequent). 
It then finds all distinct objects of non-background colors. 
For each object, it determines if it touches the border and calculates its dimensions (height/width).
It counts the number of border objects for each color.
The 'moving color' is the non-background color with the highest count of border objects (lowest numerical value breaks ties).
An output grid is initialized with the background color.
Stationary objects (non-border objects or border objects of non-moving colors) are redrawn in their original positions.
Moving objects (border objects of the 'moving color') are shifted diagonally inwards by a distance equal to their dimension (height/width), determined by their corner proximity.
"""

# Helper function to find connected components (objects) using Breadth-First Search
def find_objects(grid, colors_to_find=None):
    """
    Finds connected components (objects) of specified colors in the grid using 4-way connectivity.
    Also calculates object dimensions and top-left coordinate.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set, optional): A set of colors to find objects for. 
                                         If None, finds objects of all non-zero colors. Defaults to None.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color', 'coords', 'height', 'width', 'top_left'.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    target_colors = set(colors_to_find) if colors_to_find is not None else None

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Skip visited cells or cells not matching target colors (if specified)
            if visited[r, c] or (target_colors is not None and color not in target_colors):
                continue

            # Skip background implicitly if target_colors are non-background
            # If target_colors is None, default behaviour should skip 0 if considered background universally.
            # For this task, we explicitly pass non_background_colors, so this check is good.

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
                 # Calculate bounding box to get dimensions and top-left
                 min_r = min(r_ for r_, c_ in current_object_coords)
                 max_r = max(r_ for r_, c_ in current_object_coords)
                 min_c = min(c_ for r_, c_ in current_object_coords)
                 max_c = max(c_ for r_, c_ in current_object_coords)
                 obj_height = max_r - min_r + 1
                 obj_width = max_c - min_c + 1
                 objects.append({
                     'color': int(color), # Ensure standard int
                     'coords': current_object_coords,
                     'height': int(obj_height), # Ensure standard int
                     'width': int(obj_width), # Ensure standard int
                     'top_left': (int(min_r), int(min_c)) # Ensure standard int
                 })
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
    Uses the location of the bounding box center relative to the grid center.

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
    return int(background_color) # Ensure standard int


def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    if input_grid_np.size == 0:
        return [] # Handle empty input grid
        
    height, width = input_grid_np.shape
    grid_shape = (height, width)

    # 1. Determine background color
    background_color = find_background_color(input_grid_np)

    # 2. Find all non-background colors present in the grid
    unique_colors = np.unique(input_grid_np)
    non_background_colors = {int(c) for c in unique_colors if c != background_color}

    # If there are no non-background colors, return the input grid as is
    if not non_background_colors:
        return input_grid # Return original list format

    # 3. Find all objects composed of non-background colors
    all_objects = find_objects(input_grid_np, non_background_colors)

    # 4. Identify border objects and count them by color
    border_object_color_counts = Counter()
    object_is_border_map = {} # Store border status for quick lookup later
    for i, obj in enumerate(all_objects):
        obj_id = i # Use index as a simple ID
        is_border = is_border_object(obj['coords'], grid_shape)
        object_is_border_map[obj_id] = is_border
        if is_border:
            border_object_color_counts[obj['color']] += 1

    # 5. Determine the moving color
    moving_color = -1 # Use -1 to indicate no moving color found yet
    if border_object_color_counts:
         # Find the maximum count
         max_count = max(border_object_color_counts.values())
         # Find all colors that have this maximum count
         colors_with_max_count = [color for color, count in border_object_color_counts.items() if count == max_count]
         # Tie-breaking: choose the numerically smallest color value
         moving_color = min(colors_with_max_count) 
        
    # 6. Initialize output grid filled entirely with the background color
    output_grid = np.full_like(input_grid_np, background_color)

    # 7. Process all found non-background objects to draw onto the output grid
    for i, obj in enumerate(all_objects):
        obj_id = i
        obj_color = obj['color']
        obj_coords = obj['coords']
        obj_dim = obj['height'] # Assume square, use height as dimension for shift
        
        # Determine if this object should move
        is_border = object_is_border_map[obj_id]
        is_moving = is_border and (obj_color == moving_color)

        if is_moving:
            # Calculate shift based on corner and dimension
            corner = get_object_corner(obj_coords, grid_shape)
            dr, dc = 0, 0 # delta row, delta column for movement
            if corner == 'top-left':
                dr, dc = obj_dim, obj_dim       # Move down-right
            elif corner == 'top-right':
                dr, dc = obj_dim, -obj_dim      # Move down-left
            elif corner == 'bottom-left':
                dr, dc = -obj_dim, obj_dim      # Move up-right
            elif corner == 'bottom-right':
                dr, dc = -obj_dim, -obj_dim     # Move up-left
            
            # Apply shift to each pixel of the object and draw in the output grid
            for r, c in obj_coords:
                nr, nc = r + dr, c + dc
                # Draw the pixel at the new location, checking grid bounds
                if 0 <= nr < height and 0 <= nc < width:
                    output_grid[nr, nc] = obj_color
                # Pixels moving off-grid are implicitly handled by not drawing them

        else: 
            # Stationary object: Draw it at its original position
            for r, c in obj_coords:
                 # Check bounds (mostly for safety, should always be within bounds here)
                 if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = obj_color

    # 8. Convert the final numpy grid back to a list of lists for the required output format
    return output_grid.tolist()
```