```python
"""
Transforms an input grid based on identifying a 'frame' component (largest bounding box), 
any 'enclosed' components within the frame's box, and a 'trigger' component 
(largest bounding box among those outside the frame's box).

The composite object (frame + enclosed components) is duplicated. The duplication 
axis (horizontal or vertical) and gap size are determined by the relative position 
of the trigger component to the composite object.
- Horizontal separation -> Horizontal duplication, gap = 2 columns.
- Vertical separation -> Vertical duplication, gap = 1 row.

The output grid contains only the original composite object and its duplicate on a 
background of color 0.
"""

import numpy as np
from collections import deque

def find_objects(grid, ignore_color=0):
    """
    Finds all contiguous objects of colors other than ignore_color using BFS.
    Calculates bounding box and area for each object.

    Args:
        grid (np.array): The input grid.
        ignore_color (int): The color to treat as background.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'color' (int), 'coords' (set of tuples), 'bbox' (tuple), 'area' (int).
              Returns an empty list if no objects are found.
    """
    objects = []
    rows, cols = grid.shape
    visited = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != ignore_color and (r, c) not in visited:
                color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            coords.add((nr, nc))
                            q.append((nr, nc))
                
                if coords:
                     bbox = get_bounding_box(coords)
                     area = get_bounding_box_area(bbox)
                     objects.append({'color': color, 'coords': coords, 'bbox': bbox, 'area': area})

    return objects

def get_bounding_box(coords):
    """
    Calculates the bounding box for a set of coordinates.
    """
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return (min_r, min_c, max_r, max_c)

def get_bounding_box_area(bbox):
    """Calculates the area of a bounding box."""
    if not bbox:
        return 0
    # Ensure non-negative dimensions even for single points/lines
    height = max(0, bbox[2] - bbox[0]) + 1
    width = max(0, bbox[3] - bbox[1]) + 1
    return height * width

def get_object_center(bbox):
    """Calculates the approximate center of a bounding box."""
    if not bbox:
        return None
    center_r = (bbox[0] + bbox[2]) / 2.0
    center_c = (bbox[1] + bbox[3]) / 2.0
    return (center_r, center_c)

def extract_pattern(grid, coords, bbox):
    """
    Extracts the pixel pattern of combined objects within a bounding box.
    """
    if not bbox or not coords:
        # Return empty array if no coordinates or bounding box
        return np.array([[]], dtype=grid.dtype)
        
    min_r, min_c, max_r, max_c = bbox
    # Ensure height and width are at least 1 if coords exist
    height = max(1, max_r - min_r + 1)
    width = max(1, max_c - min_c + 1)
    
    pattern = np.zeros((height, width), dtype=grid.dtype)
    
    for r, c in coords:
        # Check if coordinate falls within the calculated bbox
        if min_r <= r <= max_r and min_c <= c <= max_c:
             # Place pixel relative to the top-left corner of the pattern grid
            pattern[r - min_r, c - min_c] = grid[r, c]
            
    return pattern

def is_bbox_inside(inner_bbox, outer_bbox):
    """Checks if inner_bbox is strictly inside or equal to outer_bbox."""
    if not inner_bbox or not outer_bbox:
        return False
    return (outer_bbox[0] <= inner_bbox[0] and 
            outer_bbox[1] <= inner_bbox[1] and
            outer_bbox[2] >= inner_bbox[2] and 
            outer_bbox[3] >= inner_bbox[3])

def is_bbox_outside(bbox1, bbox2):
    """Checks if bbox1 is completely outside bbox2 (no overlap)."""
    if not bbox1 or not bbox2:
        return True # Treat None as outside everything
    # Check for non-overlap condition
    return (bbox1[2] < bbox2[0] or  # bbox1 is entirely above bbox2
            bbox1[0] > bbox2[2] or  # bbox1 is entirely below bbox2
            bbox1[3] < bbox2[1] or  # bbox1 is entirely left of bbox2
            bbox1[1] > bbox2[3])    # bbox1 is entirely right of bbox2

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid) # Initialize with background color

    # 1. Find Components
    all_components = find_objects(input_grid, ignore_color=0)
    if not all_components:
        return output_grid # Return empty grid if no objects

    # 2. Identify Frame Component (largest BB area)
    if not all_components: # Should be caught above, but defensive check
        return output_grid
    frame_component = max(all_components, key=lambda x: x['area'])
    composite_region = frame_component['bbox'] # The BB of the largest component

    # 3. Find Enclosed Components
    enclosed_components_coords = set()
    for comp in all_components:
        if comp is frame_component: continue # Skip the frame itself
        # Check if component's BB is entirely within the frame's BB
        if is_bbox_inside(comp['bbox'], composite_region):
            enclosed_components_coords.update(comp['coords'])

    # 4. Define Composite Object
    # Combine coords from frame and all enclosed components
    composite_object_pixels = frame_component['coords'].union(enclosed_components_coords)
    # Calculate the minimal BB containing all these pixels
    composite_object_bbox = get_bounding_box(composite_object_pixels)
    # Extract the pattern within this combined BB
    composite_pattern = extract_pattern(input_grid, composite_object_pixels, composite_object_bbox)
    
    # Check if pattern extraction was successful
    if composite_pattern.size == 0 or not composite_object_bbox:
         # This might happen if frame_component had no coords - fallback or error
         print("Warning: Composite pattern extraction failed.")
         # Maybe return original or blank grid depending on desired error handling
         return output_grid 

    composite_origin_r, composite_origin_c = composite_object_bbox[0], composite_object_bbox[1]
    composite_h, composite_w = composite_pattern.shape

    # 5. Find Secondary Components (outside the composite_region defined by frame component)
    secondary_components = []
    for comp in all_components:
        # Check if component's BB is entirely outside the frame's BB
        if is_bbox_outside(comp['bbox'], composite_region):
            secondary_components.append(comp)

    # 6. Select Secondary Trigger (largest BB area among secondaries)
    if not secondary_components:
         # Fallback if no secondary component is found (as per previous logic)
         direction = 'horizontal'
         gap = 2
         # print("Warning: No secondary component found, defaulting to horizontal duplication.")
    else:
        trigger_object = max(secondary_components, key=lambda x: x['area'])
        secondary_bb = trigger_object['bbox']

        # 7. Determine Duplication Direction
        composite_center = get_object_center(composite_object_bbox)
        secondary_center = get_object_center(secondary_bb)
        
        # Basic check: primary axis of separation between centers
        delta_r = abs(secondary_center[0] - composite_center[0])
        delta_c = abs(secondary_center[1] - composite_center[1])

        # More robust check: distance between closest edges
        horizontal_gap = 0
        if composite_object_bbox[3] < secondary_bb[1]: # Secondary is to the right
            horizontal_gap = secondary_bb[1] - composite_object_bbox[3] - 1
        elif secondary_bb[3] < composite_object_bbox[1]: # Secondary is to the left
            horizontal_gap = composite_object_bbox[1] - secondary_bb[3] - 1
            
        vertical_gap = 0
        if composite_object_bbox[2] < secondary_bb[0]: # Secondary is below
            vertical_gap = secondary_bb[0] - composite_object_bbox[2] - 1
        elif secondary_bb[2] < composite_object_bbox[0]: # Secondary is above
            vertical_gap = composite_object_bbox[0] - secondary_bb[2] - 1
            
        # Determine direction based on largest separation gap between bounding boxes
        # This seems more reliable than centers for irregular shapes
        if horizontal_gap >= vertical_gap : 
            direction = 'horizontal'
        else:
            direction = 'vertical'

        # Example-specific gaps
        if direction == 'horizontal':
            gap = 2
        else: # direction == 'vertical'
            gap = 1

    # 9. Create Output Grid (already done)

    # 10. Place Original Composite Object
    # Ensure slice dimensions match pattern dimensions
    target_slice_orig = output_grid[composite_origin_r : composite_origin_r + composite_h, 
                                   composite_origin_c : composite_origin_c + composite_w]
    
    if target_slice_orig.shape == composite_pattern.shape:
        mask_orig = composite_pattern != 0
        target_slice_orig[mask_orig] = composite_pattern[mask_orig]
    else:
        print(f"Warning: Shape mismatch for original placement. Target: {target_slice_orig.shape}, Pattern: {composite_pattern.shape}")


    # 11. Calculate Placement for the Copy
    if direction == 'horizontal':
        copy_origin_r = composite_origin_r
        copy_origin_c = composite_origin_c + composite_w + gap
    else: # direction == 'vertical'
        copy_origin_r = composite_origin_r + composite_h + gap
        copy_origin_c = composite_origin_c

    # 12. Place the Copied Composite Object, checking boundaries
    copy_h, copy_w = composite_pattern.shape # Use pattern's actual shape
    
    # Calculate end coordinates, ensure they are within grid limits
    end_r = copy_origin_r + copy_h
    end_c = copy_origin_c + copy_w
    
    if (0 <= copy_origin_r < rows and 0 <= copy_origin_c < cols and
        end_r <= rows and end_c <= cols): # Check if the whole pattern fits
        
        target_slice_copy = output_grid[copy_origin_r : end_r, 
                                        copy_origin_c : end_c]

        # Double check shape match before assignment (can happen with edge cases)
        if target_slice_copy.shape == composite_pattern.shape:
            mask_copy = composite_pattern != 0
            target_slice_copy[mask_copy] = composite_pattern[mask_copy]
        else:
             print(f"Warning: Shape mismatch for copy placement. Target: {target_slice_copy.shape}, Pattern: {composite_pattern.shape}")

    # Return the final grid
    return output_grid
```