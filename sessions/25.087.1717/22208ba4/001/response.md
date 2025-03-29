```python
import numpy as np
from collections import deque

"""
Identifies contiguous objects of non-background color (orange, 7) located at the four corners of the input grid.
Determines a 'target color' based on the number of unique colors found among these corner objects and the grid dimensions:
- If 1 unique color: Target is that color.
- If 2 unique colors: Target is the minimum color if grid height and width are both odd, otherwise the maximum color.
- If 3 unique colors: Target is the median color.
Moves all corner objects matching the target color one step diagonally inwards towards the center.
The original positions of the moved objects are filled with the background color.
"""

def _find_object_coords_bfs(grid, start_row, start_col, visited):
    """
    Finds all coordinates of a connected object of the same color starting from (start_row, start_col) using BFS.
    Avoids searching the background color and already visited pixels.

    Args:
        grid (np.array): The input grid.
        start_row (int): Starting row index.
        start_col (int): Starting column index.
        visited (set): A set of (row, col) tuples already visited by previous searches.

    Returns:
        tuple: (frozenset of (row, col) coordinates for the object, object_color)
               Returns (None, None) if the start pixel is background or already visited.
    """
    height, width = grid.shape
    # Use orange (7) as the background color
    background_color = 7 

    if not (0 <= start_row < height and 0 <= start_col < width):
        return None, None # Start is out of bounds

    start_color = grid[start_row, start_col]

    if start_color == background_color or (start_row, start_col) in visited:
        return None, None # Don't process background or already processed parts

    q = deque([(start_row, start_col)])
    object_coords = set()
    visited.add((start_row, start_col)) # Mark start as visited immediately

    while q:
        r, c = q.popleft()
        object_coords.add((r, c))

        # Explore neighbors (4-directional)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, color match, and if not visited
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == start_color and (nr, nc) not in visited:
                visited.add((nr, nc)) # Mark visited when adding to queue
                q.append((nr, nc))

    return frozenset(object_coords), start_color

def _get_corner_objects_and_colors(grid):
    """
    Identifies objects located at the four corners of the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (corner_objects, unique_colors)
            - corner_objects (dict): Maps color -> list of frozensets of coordinates.
            - unique_colors (list): Sorted list of unique colors found in corner objects.
    """
    height, width = grid.shape
    corners = [(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)]
    corner_objects = {} # {color: [frozenset(coords1), frozenset(coords2), ...]}
    visited = set() # Shared visited set across all BFS calls from corners

    for r_corn, c_corn in corners:
        coords, color = _find_object_coords_bfs(grid, r_corn, c_corn, visited)
        if coords: # If an object was found (not background or already visited)
            if color not in corner_objects:
                corner_objects[color] = []
            # The visited set ensures we don't add the same object multiple times
            # if it touches more than one corner. The BFS initiated from the first
            # corner encounter will find all its coordinates. Subsequent corner
            # checks hitting the same object will return (None, None).
            corner_objects[color].append(coords)

    unique_colors = sorted(list(corner_objects.keys()))
    return corner_objects, unique_colors

def _determine_move_vector(obj_coords, H, W):
    """
    Determines the diagonal inward move vector based on which corner the object occupies.
    Assumes the object contains one of the corner pixels.

    Args:
        obj_coords (frozenset): Set of (row, col) coordinates of the object.
        H (int): Grid height.
        W (int): Grid width.

    Returns:
        tuple: (dr, dc) representing the movement vector.
    """
    if (0, 0) in obj_coords: return (1, 1)       # Top-left moves down-right
    if (0, W - 1) in obj_coords: return (1, -1)   # Top-right moves down-left
    if (H - 1, 0) in obj_coords: return (-1, 1)  # Bottom-left moves up-right
    if (H - 1, W - 1) in obj_coords: return (-1, -1)# Bottom-right moves up-left
    
    # Fallback/Error case: should not happen for corner objects found via _get_corner_objects_and_colors
    # This might occur if an object touches a corner but doesn't include the corner pixel itself,
    # which contradicts the current interpretation of examples.
    # For robustness, one could check proximity or centroid, but sticking to corner pixel containment.
    print(f"Warning: Could not determine corner for object with coords starting near {next(iter(obj_coords))}")
    return (0, 0) 

def transform(input_grid):
    """
    Transforms the input grid by moving specific corner objects diagonally inwards.

    Args:
        input_grid (np.array): The input 2D grid.

    Returns:
        np.array: The transformed 2D grid.
    """
    # Use orange (7) as the background color
    background_color = 7
    height, width = input_grid.shape
    output_grid = np.copy(input_grid)

    # 1. Identify corner objects and their unique colors
    corner_objects, unique_colors = _get_corner_objects_and_colors(input_grid)
    
    # 2. Determine the target color based on the number of unique colors (N)
    N = len(unique_colors)
    target_color = -1 # Default invalid color

    if N == 0:
        # No non-background corner objects found
        return output_grid 
    elif N == 1:
        # If only one color, that's the target
        target_color = unique_colors[0]
    elif N == 2:
        # If two colors, check grid dimensions parity
        min_color, max_color = unique_colors[0], unique_colors[1]
        if height % 2 != 0 and width % 2 != 0: # Both dimensions odd
            target_color = min_color
        else: # At least one dimension is even
            target_color = max_color
    elif N == 3:
        # If three colors, target is the median
        target_color = unique_colors[1] 
    else: 
        # Rule for N=4 or more is undefined by examples, assume no move
        print(f"Warning: Found {N} unique corner colors. Rule undefined. No objects moved.")
        return output_grid

    # 3. Identify objects matching the target color
    target_objects_coords = corner_objects.get(target_color, [])
    if not target_objects_coords:
        # Target color determined, but no objects of that color found (shouldn't happen with current logic)
        return output_grid

    # 4. Prepare for moving objects
    pixels_to_clear = set()
    pixels_to_set = [] # List of (new_row, new_col, color)

    # 5. Calculate moves for each target object
    for obj_coords in target_objects_coords:
        # Determine movement vector for this object
        dr, dc = _determine_move_vector(obj_coords, height, width)

        if dr == 0 and dc == 0: continue # Skip if no move vector determined

        # Add all original pixels to the clear set
        pixels_to_clear.update(obj_coords)

        # Calculate new positions for all pixels in the object
        for r, c in obj_coords:
            nr, nc = r + dr, c + dc
            # Check if the new position is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                 pixels_to_set.append((nr, nc, target_color))
            else:
                 # Handle cases where movement goes out of bounds (optional, current examples don't show this)
                 # Option 1: Pixel disappears (do nothing)
                 # Option 2: Pixel wraps around (not typical in ARC)
                 # Option 3: Pixel stays at boundary (not a diagonal move)
                 # Assuming Option 1 based on simplicity
                 pass


    # 6. Apply changes to the output grid
    # First, clear the original positions
    for r, c in pixels_to_clear:
        output_grid[r, c] = background_color

    # Then, set the new positions
    for nr, nc, color in pixels_to_set:
        output_grid[nr, nc] = color
        
    return output_grid
```