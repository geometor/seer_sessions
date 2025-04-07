import numpy as np
from collections import deque

"""
Identifies rectangular objects in the input grid characterized by a 1-pixel thick frame of either azure (8) or red (2), enclosing a solid rectangular core of a different color.
Moves these objects horizontally based on their frame color:
- Objects with an azure (8) frame are moved to the left edge (column 0).
- Objects with a red (2) frame are moved to the right edge (last column).
The vertical position and internal structure of the objects remain unchanged.
The background pixels are preserved, except where overwritten by moved objects.
"""

def find_objects(grid, background_color):
    """
    Finds all framed rectangular objects in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The background color.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'bbox': (min_r, min_c, max_r, max_c)
              'frame_color': The color of the frame (2 or 8)
              'subgrid': A numpy array containing the object's pixels.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # Look for potential frame pixels (red or azure) that haven't been visited
            if grid[r, c] in [2, 8] and not visited[r, c]:
                frame_color = grid[r, c]
                
                # Use BFS to find all connected pixels of the *same* frame color
                q = deque([(r, c)])
                frame_pixels = set([(r,c)])
                component_visited = set([(r, c)])
                min_r, min_c, max_r, max_c = r, c, r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore 8 neighbors (including diagonals for connectivity check)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc
                            
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == frame_color and (nr, nc) not in component_visited:
                                component_visited.add((nr, nc))
                                frame_pixels.add((nr, nc))
                                q.append((nr, nc))

                # Basic check: Potential object size must be at least 3x3
                obj_h = max_r - min_r + 1
                obj_w = max_c - min_c + 1
                if obj_h < 3 or obj_w < 3:
                    # Mark these pixels as visited to avoid reprocessing
                    for fr, fc in frame_pixels:
                        visited[fr, fc] = True
                    continue # Too small to be a framed object

                # Verify frame structure and solid core
                is_valid_object = True
                core_color = -1 # Sentinel value
                core_pixels = set()

                for ir in range(min_r, max_r + 1):
                    for ic in range(min_c, max_c + 1):
                        pixel_pos = (ir, ic)
                        pixel_val = grid[ir, ic]

                        # Check if it's on the border (frame)
                        is_border = (ir == min_r or ir == max_r or ic == min_c or ic == max_c)

                        if is_border:
                            if pixel_pos not in frame_pixels: # Should be part of the found frame component
                                is_valid_object = False
                                break
                            if pixel_val != frame_color: # Should have the correct frame color
                                 is_valid_object = False
                                 break
                        else: # Inner pixel (core)
                            if pixel_val == frame_color or pixel_val == background_color: # Core cannot be frame or background color
                                is_valid_object = False
                                break
                            if core_color == -1: # First core pixel found
                                core_color = pixel_val
                            elif pixel_val != core_color: # Core must be solid color
                                is_valid_object = False
                                break
                            core_pixels.add(pixel_pos)
                    if not is_valid_object:
                        break
                
                # Ensure the core isn't empty if the object is larger than 2x2 (which it must be)
                if core_color == -1:
                     is_valid_object = False

                # Add the object if valid
                if is_valid_object:
                    # Extract the subgrid
                    subgrid = grid[min_r:max_r+1, min_c:max_c+1]
                    objects.append({
                        'bbox': (min_r, min_c, max_r, max_c),
                        'frame_color': frame_color,
                        'subgrid': subgrid
                    })
                    # Mark all object pixels (frame and core) as visited
                    all_object_pixels = frame_pixels.union(core_pixels)
                    for orr, occ in all_object_pixels:
                         if 0 <= orr < height and 0 <= occ < width:
                            visited[orr, occ] = True
                else:
                    # Mark only the initially found frame component pixels as visited
                    # This handles cases where we find frame-colored pixels that are not part of a valid object
                    for fr, fc in frame_pixels:
                       visited[fr, fc] = True


    return objects


def transform(input_grid):
    """
    Moves framed rectangular objects horizontally based on their frame color.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Determine background color (assuming it's the color at [0, 0])
    background_color = input_np[0, 0]

    # Initialize output grid with background color
    output_grid = np.full_like(input_np, background_color)

    # Find all framed objects
    objects = find_objects(input_np, background_color)

    # Process each object
    for obj in objects:
        min_r, min_c, max_r, max_c = obj['bbox']
        frame_color = obj['frame_color']
        subgrid = obj['subgrid']
        obj_h, obj_w = subgrid.shape

        # Calculate new horizontal position
        new_c = 0
        if frame_color == 8: # Azure frame moves left
            new_c = 0
        elif frame_color == 2: # Red frame moves right
            new_c = width - obj_w
        
        # Vertical position remains the same
        new_r = min_r

        # Place the object onto the output grid
        # Ensure slicing bounds are within the grid dimensions
        end_r = min(new_r + obj_h, height)
        end_c = min(new_c + obj_w, width)
        subgrid_h = end_r - new_r
        subgrid_w = end_c - new_c
        
        if new_r < height and new_c < width and subgrid_h > 0 and subgrid_w > 0:
             output_grid[new_r:end_r, new_c:end_c] = subgrid[0:subgrid_h, 0:subgrid_w]


    return output_grid.tolist()