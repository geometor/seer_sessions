import numpy as np
import collections

"""
The transformation rule involves splitting the input grid vertically into two parts based on the first column consisting entirely of white pixels (0). 

1. Identify the left part and the right part of the grid.
2. Identify the background color of the left part (typically the color at [0, 0]).
3. Find all contiguous regions of white pixels (0) in the left part. These are the "holes". For each hole, determine its shape represented by the relative coordinates of its pixels.
4. Find all contiguous, non-white objects in the right part. For each object, determine its color and its shape (relative coordinates).
5. Match each object from the right part to a hole in the left part based on identical shapes (relative coordinates).
6. Create the output grid by copying the left part of the input grid.
7. For each matched object-hole pair, fill the pixels corresponding to the hole in the output grid with the color of the matched object.
"""

def find_objects(grid, target_color=None, background_color=None, connectivity=4):
    """
    Finds contiguous regions (objects) of a specific color or any non-background color in a grid.

    Args:
        grid (np.array): The input grid.
        target_color (int, optional): The specific color to find objects of. Defaults to None.
        background_color (int, optional): The color to ignore (treat as background).
                                          If target_color is None, finds objects of any color
                                          *not* equal to background_color. Defaults to None.
        connectivity (int): 4 or 8 way connectivity. Defaults to 4.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object and contains:
              'color': The color of the object.
              'relative_coords': A frozenset of (row, col) tuples relative to the object's top-left corner.
              'absolute_coords': A frozenset of (row, col) tuples in the original grid coordinates.
              'bbox': A tuple (min_r, min_c, max_r, max_c) representing the bounding box.
    """
    if target_color is None and background_color is None:
         background_color = 0 # Default background color if nothing else specified

    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    if connectivity == 4:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for r in range(rows):
        for c in range(cols):
            if visited[r, c]:
                continue

            pixel_color = grid[r, c]
            is_target = False

            if target_color is not None:
                # Looking for a specific color
                if pixel_color == target_color:
                    is_target = True
            elif background_color is not None:
                # Looking for anything not background
                if pixel_color != background_color:
                    is_target = True
            
            # If pixel is part of the background (and we are not specifically targeting it), skip
            if background_color is not None and pixel_color == background_color and target_color != background_color :
                 continue

            if is_target:
                # Start Breadth-First Search (BFS) to find the connected component
                component_coords = []
                q = collections.deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                current_color = pixel_color # The color of the component being traced

                while q:
                    row, col = q.popleft()
                    component_coords.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors
                    for dr, dc in deltas:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == current_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Check if a component was actually found (size > 0)
                if component_coords:
                    # Calculate relative coordinates based on the bounding box top-left
                    relative_coords = frozenset((rr - min_r, cc - min_c) for rr, cc in component_coords)
                    absolute_coords = frozenset(component_coords)

                    objects.append({
                        'color': current_color,
                        'relative_coords': relative_coords,
                        'absolute_coords': absolute_coords,
                        'bbox': (min_r, min_c, max_r, max_c)
                    })
                    
    return objects

def split_grid(grid):
    """Splits the grid vertically based on the first all-white column."""
    rows, cols = grid.shape
    split_col = -1
    white_color = 0 # Define white color
    for c in range(cols):
        if np.all(grid[:, c] == white_color):
            split_col = c
            break
            
    if split_col == -1:
        # If no split column found, maybe the pattern is different or it's the whole grid
        # For this task, assume the split always exists as per examples.
        # Alternatively, could return grid, None or raise error
         raise ValueError("No separating white column found in the grid.")

    left_grid = grid[:, :split_col]
    # Ensure there's content to the right of the split column before slicing
    if split_col + 1 < cols:
        right_grid = grid[:, split_col + 1:]
    else:
        right_grid = np.array([[]] * rows) # Empty grid if split is at the last column

    return left_grid, right_grid

def transform(input_grid):
    """
    Applies the transformation rule: identifies holes in the left part and objects
    in the right part of the input grid based on a white separator column,
    matches them by shape, and fills the holes with the corresponding object colors.
    """
    # 1. Split the grid
    left_grid, right_grid = split_grid(input_grid)
    
    # Initialize output grid as a copy of the left part
    output_grid = np.copy(left_grid)
    
    # Define white color (holes) and background color for objects on the right
    white_color = 0
    
    # 3. Find holes (white regions) in the left grid
    # We are looking for contiguous regions of 'white_color'
    holes = find_objects(left_grid, target_color=white_color)
    
    # 4. Find non-white objects in the right grid
    # We are looking for anything that isn't 'white_color'
    objects = find_objects(right_grid, background_color=white_color)

    # 5. Match objects to holes based on shape (relative coordinates)
    # Create a dictionary for holes based on their shape for faster lookup
    holes_by_shape = {hole['relative_coords']: hole for hole in holes}

    # 6. Fill holes in the output grid
    for obj in objects:
        obj_shape = obj['relative_coords']
        obj_color = obj['color']
        
        # Find the matching hole by shape
        if obj_shape in holes_by_shape:
            matching_hole = holes_by_shape[obj_shape]
            
            # Iterate through the absolute coordinates of the hole and fill with object color
            for r, c in matching_hole['absolute_coords']:
                # Ensure coordinates are within the bounds of the output grid (should be)
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                    output_grid[r, c] = obj_color
            
            # Optional: remove matched hole to prevent multiple matches if shapes were identical
            # del holes_by_shape[obj_shape] 
        # else:
            # Handle cases where an object shape doesn't match any hole shape (optional)
            # print(f"Warning: Object with color {obj_color} and shape {obj_shape} did not match any hole.")

    return output_grid