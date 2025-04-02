import numpy as np
from collections import deque
import itertools

"""
Transforms an input grid by duplicating a composite structure (a 'container' object 
and the 'contained' objects within its bounding box) to a new location. The new 
location is determined by the position of an 'orphan' object, typically one that 
shares characteristics (like color) with a contained object. The process involves:
1. Identifying all distinct objects (contiguous non-white pixels).
2. Identifying the 'container' object, defined as an object whose bounding box 
   inclusively encloses the bounding box of at least one other object of a 
   different color.
3. Identifying 'contained' objects enclosed within the container's bounding box.
4. Identifying 'orphan' objects (neither container nor contained).
5. Selecting a 'primary orphan' (often matching a contained object's color) to 
   dictate placement.
6. Calculating the target location for the copy, maintaining a 2-pixel gap from 
   the primary orphan's original position.
7. Creating an output grid by copying the input.
8. Removing all orphan objects from the output grid.
9. Extracting the pattern (container's bounding box region) from the original input.
10. Pasting the pattern onto the output grid at the target location.
"""

# === Helper Functions ===

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid using Breadth-First Search.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dicts, where each dict represents an object and contains:
              - 'id': A unique integer identifier for the object.
              - 'coords': set of (row, col) coordinates.
              - 'bbox': tuple (min_r, min_c, max_r, max_c).
              - 'color': int color value.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    object_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]: # Found unvisited non-background pixel
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c, max_r, max_c = r, c, r, c # Initialize bounding box

                # Perform BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    # Update bounding box
                    min_r, min_c = min(min_r, row), min(min_c, col)
                    max_r, max_c = max(max_r, row), max(max_c, col)

                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, visited status, and color match
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Store the found object if it has coordinates
                if obj_coords:
                    bounding_box = (min_r, min_c, max_r, max_c)
                    objects.append({'id': object_id_counter, 'coords': obj_coords, 'bbox': bounding_box, 'color': color})
                    object_id_counter += 1
    return objects

def is_inclusively_enclosed(inner_box, outer_box):
    """
    Checks if inner_box is inclusively inside outer_box (edges can touch).
    Requires the boxes to be distinct objects (checked by caller via IDs).

    Args:
        inner_box (tuple): Bbox (min_r, min_c, max_r, max_c).
        outer_box (tuple): Bbox (min_r, min_c, max_r, max_c).

    Returns:
        bool: True if inner_box is enclosed by outer_box, False otherwise.
    """
    # An object cannot enclose itself - this check prevents identical boxes from qualifying
    if inner_box == outer_box:
        return False
    min_r1, min_c1, max_r1, max_c1 = inner_box
    min_r2, min_c2, max_r2, max_c2 = outer_box
    # Check if all inner bounds are within or equal to outer bounds
    return min_r1 >= min_r2 and min_c1 >= min_c2 and max_r1 <= max_r2 and max_c1 <= max_c2

# === Main Transformation Function ===

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify all distinct objects
    all_objects = find_objects(input_np)
    if not all_objects:
        return input_grid # Return original if no objects

    # 2. & 3. Identify Container and Contained Objects
    container = None
    contained_objects_map = {} # Store {container_id: [list of contained_obj dicts]}
    potential_containers = []

    # Find all objects that enclose at least one other object of a different color
    for obj_i in all_objects:
        current_contained = []
        for obj_j in all_objects:
            # Skip self-comparison
            if obj_i['id'] == obj_j['id']:
                continue
            # Check for enclosure AND different colors
            if obj_i['color'] != obj_j['color'] and is_inclusively_enclosed(obj_j['bbox'], obj_i['bbox']):
                 current_contained.append(obj_j) # obj_j is contained within obj_i

        # If obj_i encloses any object of a different color, it's a potential container
        if current_contained:
             contained_objects_map[obj_i['id']] = current_contained
             potential_containers.append(obj_i)

    # Select the container (simple strategy: first found)
    if potential_containers:
        container = potential_containers[0]
    else:
        # If no object encloses another of a different color, cannot proceed
        # print("Warning: No container found meeting criteria.") # Optional debug
        return input_grid

    container_id = container['id']
    container_bbox = container['bbox']
    # Get the list of objects contained by the chosen container
    contained_objects = contained_objects_map.get(container_id, [])
    contained_ids = {obj['id'] for obj in contained_objects}
    contained_colors = {obj['color'] for obj in contained_objects}

    # 4. Identify Orphan Objects
    orphan_objects = []
    for obj in all_objects:
        # An object is an orphan if it's not the container AND not contained by the container
        if obj['id'] != container_id and obj['id'] not in contained_ids:
            orphan_objects.append(obj)

    if not orphan_objects:
        # If only container + contained exist, cannot determine placement
        # print("Warning: Container and contained objects found, but no orphans.") # Optional debug
        return input_grid # Needs an orphan to determine placement

    # 5. Select Primary Orphan
    primary_orphan = None
    # Prioritize an orphan whose color matches any contained object's color
    for orphan in orphan_objects:
        if orphan['color'] in contained_colors:
            primary_orphan = orphan
            break # Use the first matching orphan found

    # Fallback: If no color match, use the first orphan identified
    if primary_orphan is None and orphan_objects:
        primary_orphan = orphan_objects[0]

    # If still no primary orphan (should only happen if orphan_objects was empty initially)
    if primary_orphan is None:
         # print("Error: Failed to select a primary orphan.") # Optional debug
         return input_grid # Should have been caught earlier

    orphan_bbox = primary_orphan['bbox']

    # 6. Calculate Target Location for the Copy
    c_min_r, c_min_c, c_max_r, c_max_c = container_bbox
    o_min_r, o_min_c, o_max_r, o_max_c = orphan_bbox
    target_row, target_col = -1, -1 # Initialize target coordinates

    # Determine relative position based on non-overlapping bounding boxes
    is_below = o_min_r > c_max_r
    is_right = o_min_c > c_max_c
    is_above = o_max_r < c_min_r
    is_left = o_max_c < c_min_c

    # Calculate placement coordinates with a 2-pixel gap
    if is_below:
        target_row = o_min_r - 2 # Place top edge 2 pixels above orphan's top edge
        target_col = c_min_c     # Align left edge with container's left edge
    elif is_right:
        target_row = c_min_r     # Align top edge with container's top edge
        target_col = o_min_c - 2 # Place left edge 2 pixels left of orphan's left edge
    elif is_above: # Added for potential future cases
        target_row = o_max_r + 2 # Place top edge 2 pixels below orphan's bottom edge
        target_col = c_min_c     # Align left edge
    elif is_left: # Added for potential future cases
        target_row = c_min_r     # Align top edge
        target_col = o_max_c + 2 # Place left edge 2 pixels right of orphan's right edge
    else:
        # Handle ambiguous/overlapping cases if necessary (not seen in examples)
        # print(f"Warning: Ambiguous relative position between container {container_bbox} and primary orphan {orphan_bbox}.") # Optional debug
        return input_grid # Cannot determine placement based on rules

    # 7. Create Output Grid (start with a copy of input)
    output_np = np.copy(input_np)

    # 8. Remove ALL Orphan Objects from the output grid
    for orphan in orphan_objects:
        for r, c in orphan['coords']:
            # Ensure coordinates are within bounds before modifying
            if 0 <= r < rows and 0 <= c < cols:
                output_np[r, c] = 0 # Set orphan pixels to background color (0)

    # 9. Extract the Pattern (Container BBox region) from the ORIGINAL Input Grid
    pattern = input_np[c_min_r : c_max_r + 1, c_min_c : c_max_c + 1]
    pattern_h, pattern_w = pattern.shape

    # 10. Place the Extracted Pattern onto the Output Grid (with Clipping)
    # Check if target coordinates and pattern dimensions are valid
    if target_row != -1 and target_col != -1 and pattern_h > 0 and pattern_w > 0:
        # Define the target slice range in the output grid
        end_row = target_row + pattern_h
        end_col = target_col + pattern_w

        # Calculate actual paste boundaries, respecting grid limits (clipping)
        paste_start_row = max(0, target_row)
        paste_start_col = max(0, target_col)
        paste_end_row = min(rows, end_row)
        paste_end_col = min(cols, end_col)

        # Calculate the corresponding slice from the pattern to be copied
        pattern_start_row = max(0, -target_row) # Offset if target_row is negative
        pattern_start_col = max(0, -target_col) # Offset if target_col is negative
        pattern_end_row = pattern_start_row + (paste_end_row - paste_start_row)
        pattern_end_col = pattern_start_col + (paste_end_col - paste_start_col)

        # Proceed with pasting only if the calculated slices have positive dimensions
        if paste_start_row < paste_end_row and paste_start_col < paste_end_col:
            output_np[paste_start_row:paste_end_row, paste_start_col:paste_end_col] = \
                pattern[pattern_start_row:pattern_end_row, pattern_start_col:pattern_end_col]
        # else: # Optional debug for clipping issues
            # print(f"Warning: Calculated placement ({target_row},{target_col}) resulted in no valid area to paste after clipping.")

    # else: # Optional debug for invalid target/pattern issues
        # print("Warning: Invalid target coordinates or pattern dimensions prevented pasting.")

    # Convert the final NumPy array back to a list of lists for the required output format
    return output_np.tolist()