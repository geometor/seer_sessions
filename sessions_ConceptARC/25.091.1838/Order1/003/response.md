Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

"""
Transforms the input grid by rearranging objects based on their spatial arrangement.

1.  Identifies distinct non-white objects in the input grid, recording their color, 
    relative pixel coordinates (to bounding box top-left), and bounding box.
2.  Determines if the objects are primarily arranged horizontally or vertically by 
    checking bounding box separation. Sorts objects along this primary axis.
3.  Calculates the gaps (number of background cells) between adjacent objects along 
    the arrangement axis in their original sorted order.
4.  Determines a permutation of the object indices based on the arrangement axis:
    - If Horizontal: Performs a left cyclic shift on the indices of the first N-1 
      objects (0->1, 1->2, ..., N-2 -> 0), leaving the last object's index in place.
    - If Vertical: Reverses the order of the object indices.
5.  Calculates the new top-left drawing coordinates for each object based on the 
    permuted sequence, original object dimensions, and original gaps between them. 
    Objects are aligned along the non-arrangement axis based on the minimum 
    coordinate observed across all objects along that axis.
6.  Reconstructs the output grid by drawing the original objects (using their 
    relative pixels) at their newly calculated top-left positions on a background grid.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (relative coordinates), and 'bbox'.
              Returns empty list if no objects are found.
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    background_color = 0 # Assuming 0 is always background

    for r in range(height):
        for c in range(width):
            # Check if pixel is part of an object and not visited yet
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                q = deque([(r, c)]) # Queue for BFS
                visited[r, c] = True
                object_pixels_abs = set([(r, c)]) # Store absolute coordinates
                # Initialize bounding box coordinates
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and if visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            object_pixels_abs.add((nr, nc))

                # Convert absolute pixel coordinates to relative coordinates (to bbox top-left)
                object_pixels_rel = set((px_r - min_r, px_c - min_c) for px_r, px_c in object_pixels_abs)
                bbox = (min_r, min_c, max_r, max_c)
                objects.append({
                    'color': color,
                    'pixels': object_pixels_rel,
                    'bbox': bbox
                    # 'orig_index' will be added later after sorting
                })
    return objects

def determine_arrangement_and_sort(objects):
    """
    Determines arrangement axis, sorts objects, calculates gaps, and adds original index.

    Args:
        objects (list): List of object dictionaries from find_objects.

    Returns:
        tuple: (arrangement_axis, sorted_objects, gaps)
               arrangement_axis (str): 'horizontal', 'vertical', or 'none'.
               sorted_objects (list): Objects sorted by arrangement axis, each dict
                                      now includes 'orig_index'.
               gaps (list): Gaps (>=0) between adjacent sorted objects along the axis.
                            len(gaps) == len(sorted_objects) - 1.
    """
    num_objects = len(objects)
    # Base case: 0 or 1 object, no arrangement or gaps
    if num_objects <= 1:
        for i, obj in enumerate(objects):
             obj['orig_index'] = i
        return 'none', objects, []

    # Calculate potential overlaps/separations for both axes
    # Sort by min_c (left edge) for horizontal analysis
    objects_sorted_c = sorted(objects, key=lambda o: o['bbox'][1])
    # Sort by min_r (top edge) for vertical analysis
    objects_sorted_r = sorted(objects, key=lambda o: o['bbox'][0])

    h_overlaps = 0
    h_gaps = []
    for i in range(num_objects - 1):
        # bbox = (min_r, min_c, max_r, max_c)
        max_c_prev = objects_sorted_c[i]['bbox'][3]
        min_c_next = objects_sorted_c[i+1]['bbox'][1]
        # Check for horizontal overlap or touching
        if max_c_prev >= min_c_next -1 : # Treat touching as overlap for simplicity? Check examples. Example 1 has gaps. Let's require a gap > 0.
             if max_c_prev >= min_c_next: # Bboxes overlap horizontally
                 h_overlaps += 1
                 h_gaps.append(0) # Represent overlap as 0 gap for calculation? Or maybe 1? Let's stick to 0 for now. Or better, use 1 as minimum gap even if they overlapped.
             else: # Touching exactly
                 h_gaps.append(0)
        else: # Clear gap exists
            h_gaps.append(min_c_next - max_c_prev - 1)

    v_overlaps = 0
    v_gaps = []
    for i in range(num_objects - 1):
        max_r_prev = objects_sorted_r[i]['bbox'][2]
        min_r_next = objects_sorted_r[i+1]['bbox'][0]
        # Check for vertical overlap or touching
        if max_r_prev >= min_r_next -1:
            if max_r_prev >= min_r_next: # Bboxes overlap vertically
                v_overlaps += 1
                v_gaps.append(0) # Treat overlap as 0 gap
            else: # Touching exactly
                 v_gaps.append(0)
        else: # Clear gap exists
            v_gaps.append(min_r_next - max_r_prev - 1)

    # Determine primary arrangement axis
    # Prioritize the axis with zero overlaps if the other has overlaps
    if h_overlaps == 0 and v_overlaps > 0:
        arrangement = 'horizontal'
    elif v_overlaps == 0 and h_overlaps > 0:
        arrangement = 'vertical'
    # If both have overlaps or both have no overlaps, decide based on which has fewer overlaps
    # (or default to horizontal if equal)
    elif h_overlaps <= v_overlaps:
         arrangement = 'horizontal'
    else: # v_overlaps < h_overlaps
         arrangement = 'vertical'

    # Assign the final sorted list and corresponding gaps based on the chosen axis
    if arrangement == 'horizontal':
        sorted_objects = objects_sorted_c
        gaps = h_gaps
    elif arrangement == 'vertical':
        sorted_objects = objects_sorted_r
        gaps = v_gaps
    else: # Should not be reached if num_objects > 1, defensive fallback
        # Sort by top-then-left as a default order
        sorted_objects = sorted(objects, key=lambda o: (o['bbox'][0], o['bbox'][1]))
        gaps = []
        arrangement = 'none'

    # Add original index to each object based on the chosen sorted order
    # This index refers to its position (0 to N-1) in the sorted list
    for i, obj in enumerate(sorted_objects):
        obj['orig_index'] = i

    # Ensure gaps are non-negative for calculation (treat overlaps/touching as gap=0 or 1?)
    # Example 1 has gaps > 0. Let's assume minimum gap of 1 if original was <= 0.
    final_gaps = [max(1, g) if g <= 0 else g for g in gaps] # Use original gap if > 0, else use 1

    # Recalculate gaps just based on bbox distance, ensuring positive.
    final_gaps = []
    if arrangement == 'horizontal':
        for i in range(num_objects - 1):
            gap = sorted_objects[i+1]['bbox'][1] - sorted_objects[i]['bbox'][3] - 1
            final_gaps.append(max(0, gap)) # Ensure gap is never negative
    elif arrangement == 'vertical':
        for i in range(num_objects - 1):
            gap = sorted_objects[i+1]['bbox'][0] - sorted_objects[i]['bbox'][2] - 1
            final_gaps.append(max(0, gap))


    return arrangement, sorted_objects, final_gaps


def transform(input_grid):
    """
    Applies the object rearrangement transformation to the input grid.
    """
    # Initialize output_grid with the same dimensions and background color
    output_grid = np.zeros_like(input_grid)
    background_color = 0
    output_grid.fill(background_color)

    # 1. Find all distinct objects
    objects_found = find_objects(input_grid)
    num_objects = len(objects_found)

    # If no objects, return the empty grid
    if num_objects == 0:
        return output_grid

    # 2. Determine arrangement axis, sort objects, calculate gaps, add original index
    arrangement_axis, objects, gaps = determine_arrangement_and_sort(objects_found)

    # Handle base case: 0 or 1 object, or no clear arrangement determined
    # Just redraw the object(s) in their original positions
    if num_objects <= 1 or arrangement_axis == 'none':
        for obj in objects: # 'objects' is the sorted list, but order doesn't matter here
            min_r, min_c, _, _ = obj['bbox'] # Get original top-left corner
            color = obj['color']
            # Draw the object using its relative pixels from its original position
            for rel_r, rel_c in obj['pixels']:
                draw_r, draw_c = min_r + rel_r, min_c + rel_c
                # Check grid bounds before drawing
                if 0 <= draw_r < output_grid.shape[0] and 0 <= draw_c < output_grid.shape[1]:
                    output_grid[draw_r, draw_c] = color
        return output_grid

    # 4. Determine the permutation of original indices based on the arrangement axis
    original_indices = list(range(num_objects)) # Indices [0, 1, ..., N-1] based on sorted order
    permuted_indices = list(original_indices) # Start with identity, will be modified

    if arrangement_axis == 'horizontal':
        # Apply Left cyclic shift to the first N-1 indices:
        # The object originally at index 0 moves to index 1's slot,
        # object at 1 moves to 2's slot, ..., object at N-2 moves to 0's slot.
        # The object originally at index N-1 stays in index N-1's slot.
        # Result: permuted_indices[new_slot] = original_index
        if num_objects > 1:
            first_idx = original_indices[0] # Index of the first object in sorted list
            # Shift indices 1 to N-1 one step to the left (into slots 0 to N-2)
            for i in range(num_objects - 2): # Iterate through target slots 0 to N-3
                permuted_indices[i] = original_indices[i+1]
            # Place the first object's index into the second-to-
---
