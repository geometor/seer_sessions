```python
import numpy as np
from collections import deque

"""
Identifies two static yellow (4) 'anchor' objects and one other uniquely colored 'mover' object against an orange (7) background.
Determines which anchor the mover is initially closest to (Source Anchor) and the other anchor (Target Anchor).
Calculates the relative quadrant (NW, NE, SW, SE) of the mover with respect to the Source Anchor's center.
Calculates the target position for the mover, which is adjacent to the Target Anchor in the diagonally opposite quadrant relative to the Target Anchor's bounding box.
Creates the output grid by erasing the mover from its original position (filling with the background color) and drawing it in the new calculated position.
"""

def find_objects(grid, ignore_color=None):
    """
    Finds connected components of the same color in the grid.
    Returns a list of objects, where each object is a dictionary containing
    'color', 'coords' (list of (r, c) tuples), 'bbox' (min_r, min_c, max_r, max_c),
    and 'center' (r, c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                if ignore_color is not None and color == ignore_color:
                    visited[r, c] = True
                    continue

                coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                sum_r, sum_c = 0, 0

                while q:
                    row, col = q.popleft()
                    coords.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)
                    sum_r += row
                    sum_c += col

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if coords: # Only add if we found coordinates (i.e., not just background we skipped)
                    center_r = sum_r / len(coords)
                    center_c = sum_c / len(coords)
                    objects.append({
                        'color': color,
                        'coords': coords,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'center': (center_r, center_c)
                    })
    return objects

def calculate_distance(center1, center2):
    """Calculates Euclidean distance between two center points."""
    r1, c1 = center1
    r2, c2 = center2
    return np.sqrt((r1 - r2)**2 + (c1 - c2)**2)

def get_relative_quadrant(center_obj, center_ref):
    """Determines the quadrant (NW, NE, SW, SE) of center_obj relative to center_ref."""
    obj_r, obj_c = center_obj
    ref_r, ref_c = center_ref
    
    north = obj_r < ref_r
    south = obj_r > ref_r
    west = obj_c < ref_c
    east = obj_c > ref_c

    # Handle cases exactly on axis by slightly preferring N/S over E/W, then N over S, W over E
    if not north and not south: # Exactly horizontal
        north = True # Arbitrarily pick North
    if not west and not east: # Exactly vertical
        west = True # Arbitrarily pick West
        
    if north and west: return "NW"
    if north and east: return "NE"
    if south and west: return "SW"
    if south and east: return "SE"
    # Default/fallback if alignment is perfect (should be covered above)
    return "SE" 

def get_opposite_quadrant(quadrant):
    """Returns the diagonally opposite quadrant."""
    if quadrant == "NW": return "SE"
    if quadrant == "NE": return "SW"
    if quadrant == "SW": return "NE"
    if quadrant == "SE": return "NW"
    return None # Should not happen

def get_mover_relative_coords(coords):
    """ Converts absolute coords to coords relative to the top-left corner. """
    if not coords:
        return [], (0,0)
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    relative_coords = [(r - min_r, c - min_c) for r, c in coords]
    return relative_coords, (min_r, min_c)


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Make a copy to modify
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Define known colors
    background_color = 7
    anchor_color = 4

    # Find all non-background objects
    objects = find_objects(output_grid, ignore_color=background_color)

    # Identify anchors and mover
    anchors = [obj for obj in objects if obj['color'] == anchor_color]
    movers = [obj for obj in objects if obj['color'] != anchor_color]

    # Basic validation
    if len(anchors) != 2 or len(movers) != 1:
        # Return original grid if assumptions aren't met
        # Or raise an error, depending on desired behavior for unexpected input
        print(f"Warning: Expected 2 anchors and 1 mover, found {len(anchors)} anchors and {len(movers)} movers.")
        return output_grid 
        
    mover = movers[0]
    anchor1, anchor2 = anchors[0], anchors[1]

    # Determine source and target anchors
    dist1 = calculate_distance(mover['center'], anchor1['center'])
    dist2 = calculate_distance(mover['center'], anchor2['center'])

    if dist1 <= dist2:
        source_anchor = anchor1
        target_anchor = anchor2
    else:
        source_anchor = anchor2
        target_anchor = anchor1

    # Determine initial relative quadrant
    initial_quadrant = get_relative_quadrant(mover['center'], source_anchor['center'])

    # Determine target quadrant
    target_quadrant = get_opposite_quadrant(initial_quadrant)

    # Get mover shape relative to its top-left corner
    mover_rel_coords, mover_orig_top_left = get_mover_relative_coords(mover['coords'])
    mover_height = max(r for r, c in mover_rel_coords) + 1 if mover_rel_coords else 0
    mover_width = max(c for r, c in mover_rel_coords) + 1 if mover_rel_coords else 0

    # Get target anchor bounding box
    tr_min, tc_min, tr_max, tc_max = target_anchor['bbox']

    # Calculate new top-left position based on target quadrant and anchor bbox
    new_r, new_c = 0, 0
    if target_quadrant == "NW":
        new_r = tr_min - mover_height
        new_c = tc_min - mover_width
    elif target_quadrant == "NE":
        new_r = tr_min - mover_height
        new_c = tc_max + 1
    elif target_quadrant == "SW":
        new_r = tr_max + 1
        new_c = tc_min - mover_width
    elif target_quadrant == "SE":
        new_r = tr_max + 1
        new_c = tc_max + 1
        
    # --- Grid Modification ---

    # Erase mover from original position
    for r, c in mover['coords']:
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = background_color

    # Draw mover at new position
    mover_color = mover['color']
    for r_off, c_off in mover_rel_coords:
        draw_r, draw_c = new_r + r_off, new_c + c_off
        # Check bounds before drawing
        if 0 <= draw_r < rows and 0 <= draw_c < cols:
            output_grid[draw_r, draw_c] = mover_color
        else:
             # This case should ideally not happen based on ARC constraints/examples
             # but good to be aware of potential out-of-bounds placement
             print(f"Warning: Calculated draw position ({draw_r}, {draw_c}) is out of bounds.")


    return output_grid
```