```python
import numpy as np
from collections import deque

"""
Identifies specific rectangular objects within the input grid and moves them horizontally based on their frame color.

Objects are defined as having:
1.  A minimum size of 3x3.
2.  A 1-pixel thick, perfectly rectangular frame of either azure (8) or red (2).
3.  A solid rectangular core completely enclosed by the frame.
4.  The core color must be different from both the frame color and the grid's background color.

Transformation Steps:
1.  Determine the background color of the input grid (assumed from the top-left corner).
2.  Initialize an output grid of the same dimensions, filled entirely with the background color.
3.  Find all qualifying framed rectangular objects in the input grid.
4.  For each found object:
    a.  Determine its frame color and its original pixel data (subgrid).
    b.  Keep its original vertical position (top row).
    c.  Calculate the new horizontal position (left column) based on the frame color:
        - Azure (8) frames move to the left edge (column 0).
        - Red (2) frames move to the right edge (last column).
    d.  Draw the object's original pixel data (subgrid) onto the output grid at its new calculated position.
5.  Return the completed output grid. Pixels not part of any moved object remain as the background color.
"""

def _find_objects(grid, background_color):
    """
    Internal helper function to find all framed rectangular objects matching the criteria.

    Args:
        grid (np.array): The input grid.
        background_color (int): The background color.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'bbox': (min_r, min_c, max_r, max_c) - Original bounding box
              'frame_color': The color of the frame (2 or 8)
              'subgrid': A numpy array containing the object's pixels.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # Potential starting pixel for a frame? Must be Red(2) or Azure(8), not background, and not visited
            if grid[r, c] in [2, 8] and grid[r, c] != background_color and not visited[r, c]:
                frame_color = grid[r, c]
                
                # --- Step 1: BFS to find connected component of the frame color ---
                q = deque([(r, c)])
                component_pixels = set([(r, c)]) # Pixels belonging to this connected component
                component_visited_bfs = set([(r, c)]) # Track visited *during this specific BFS*
                min_r_bfs, min_c_bfs, max_r_bfs, max_c_bfs = r, c, r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    min_r_bfs = min(min_r_bfs, curr_r)
                    min_c_bfs = min(min_c_bfs, curr_c)
                    max_r_bfs = max(max_r_bfs, curr_r)
                    max_c_bfs = max(max_c_bfs, curr_c)

                    # Explore 8 neighbors (cardinal + diagonal)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc
                            
                            # Check bounds, same color, and not visited in *this* BFS run
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == frame_color and (nr, nc) not in component_visited_bfs:
                                component_visited_bfs.add((nr, nc))
                                component_pixels.add((nr, nc))
                                q.append((nr, nc))
                
                # --- Step 2: Define Bounding Box and Basic Size Check ---
                min_r, min_c, max_r, max_c = min_r_bfs, min_c_bfs, max_r_bfs, max_c_bfs
                obj_h = max_r - min_r + 1
                obj_w = max_c - min_c + 1

                # Must be at least 3x3 to have a frame and core
                if obj_h < 3 or obj_w < 3:
                    # Mark the found component pixels as globally visited and continue
                    for fr, fc in component_pixels:
                         if 0 <= fr < height and 0 <= fc < width: # boundary check just in case
                            visited[fr, fc] = True
                    continue 

                # --- Step 3: Validate Frame and Core Structure ---
                is_valid_object = True
                core_color = -1 # Sentinel value, indicates core color not yet found
                
                # Check every pixel within the bounding box derived from the BFS component
                for ir in range(min_r, max_r + 1):
                    for ic in range(min_c, max_c + 1):
                        pixel_val = grid[ir, ic]
                        is_on_border = (ir == min_r or ir == max_r or ic == min_c or ic == max_c)

                        if is_on_border:
                            # Border pixels MUST match the frame color found
                            if pixel_val != frame_color:
                                is_valid_object = False
                                break
                        else: # Inner pixel (potential core)
                            # Core pixel cannot be the frame color or the background color
                            if pixel_val == frame_color or pixel_val == background_color:
                                is_valid_object = False
                                break
                            # Check for solid core color consistency
                            if core_color == -1: # First valid core pixel found
                                core_color = pixel_val
                            elif pixel_val != core_color: # Subsequent core pixels must match
                                is_valid_object = False
                                break
                    if not is_valid_object:
                        break # Exit outer loop if invalidity found

                # Final check: a core color must have been identified (not hollow)
                if core_color == -1:
                     is_valid_object = False

                # --- Step 4: Process Valid/Invalid Object ---
                if is_valid_object:
                    # Extract the object's pixel data (subgrid)
                    subgrid = grid[min_r:max_r+1, min_c:max_c+1]
                    objects.append({
                        'bbox': (min_r, min_c, max_r, max_c),
                        'frame_color': frame_color,
                        'subgrid': subgrid
                    })
                    # Mark all pixels *within the bounding box* of the valid object as globally visited
                    visited[min_r:max_r+1, min_c:max_c+1] = True
                else:
                    # If validation failed, only mark the specific pixels found in the initial BFS component as visited
                    # This prevents marking large areas based on an invalid structure
                    for fr, fc in component_pixels:
                         if 0 <= fr < height and 0 <= fc < width:
                            visited[fr, fc] = True

    return objects


def transform(input_grid):
    """
    Applies the transformation rule to the input grid. Finds framed objects
    (red or azure frame, solid different-colored core) and moves them
    horizontally to the grid edges based on frame color (azure->left, red->right),
    preserving vertical position.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Determine background color (assuming top-left pixel is representative)
    # Add simple check in case top-left is part of an object frame
    background_color = input_np[0,0]
    if background_color in [2, 8]: # if top-left is frame color, check neighbor
        if width > 1:
            background_color = input_np[0,1]
        elif height > 1:
            background_color = input_np[1,0]
        # If still ambiguous, default might be needed, but examples suggest simple check is okay.
        # A more robust method would be mode calculation, but let's stick to simple for now.

    # Initialize the output grid filled with the background color
    output_grid = np.full_like(input_np, background_color)

    # Find all qualifying framed objects in the input grid
    objects_to_move = _find_objects(input_np, background_color)

    # Process each identified object
    for obj in objects_to_move:
        min_r, _, _, _ = obj['bbox'] # Only need original top row
        frame_color = obj['frame_color']
        subgrid = obj['subgrid']
        obj_h, obj_w = subgrid.shape

        # Calculate new target horizontal position (column)
        new_c = 0 # Default target: left edge (for azure frame)
        if frame_color == 2: # Red frame moves to the right edge
            new_c = width - obj_w
        
        # Vertical position remains unchanged from the original object's top row
        new_r = min_r

        # Calculate the slice boundaries for placing the object in the output grid
        end_r = new_r + obj_h
        end_c = new_c + obj_w

        # Place (draw) the object's subgrid onto the output grid at the new position
        # Basic bounds check before assignment (though logic should prevent out-of-bounds)
        if 0 <= new_r < height and end_r <= height and 0 <= new_c < width and end_c <= width:
             output_grid[new_r:end_r, new_c:end_c] = subgrid

    # Convert the final numpy array back to a standard list of lists for the output
    return output_grid.tolist()
```