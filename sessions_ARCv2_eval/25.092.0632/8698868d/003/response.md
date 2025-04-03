```python
import numpy as np
from collections import deque

"""
Identify distinct colored shapes (frames) separated by a background/noise color. 
Group these frames into two sets (Targets and Sources) based on spatial arrangement 
and potentially other properties like noise presence or size. Pair Target frames 
with Source frames based on relative position within their groups. For each Target 
frame, replace pixels matching the noise color *within its bounding box* with the 
solid color of its paired Source frame. Assemble the modified Target frames into 
the output grid, maintaining their relative spatial arrangement.
"""

# --- Helper Function: Find Objects ---
def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid.
    Uses Breadth-First Search (BFS).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color', 'coords' (set of (r, c) tuples),
              'bbox' (min_r, max_r, min_c, max_c), and 'size'.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r, min_c, max_c = r, r, c, c

                while q:
                    row, col = q.popleft()
                    coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if len(coords) > 0:
                    objects.append({
                        'color': color,
                        'coords': coords,
                        'bbox': (min_r, max_r, min_c, max_c),
                        'size': len(coords)
                    })
    return objects

# --- Helper Function: Determine Noise Color ---
def determine_noise_color(grid, objects):
    """
    Determines the noise/background color using heuristics.
    Checks for colors frequently appearing inside the bounding boxes of other objects,
    but not part of the object itself. Falls back to most frequent color if needed.

    Args:
        grid (np.array): The input grid.
        objects (list): List of objects found by find_objects.

    Returns:
        int: The determined noise color.
    """
    counts_inside_others = {}
    non_noise_candidate_objects = [obj for obj in objects if obj['size'] > 1] # Ignore single pixels initially

    for obj in non_noise_candidate_objects:
        min_r, max_r, min_c, max_c = obj['bbox']
        obj_color = obj['color']
        # Check pixels *within* bbox but *not* part of the object
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if (r, c) not in obj['coords']:
                    pixel_color = grid[r, c]
                    # Ensure this 'inside' pixel isn't part of another known large object
                    is_part_of_other_obj = False
                    for other_obj in non_noise_candidate_objects:
                         # Check if the pixel belongs to another object AND that object isn't the current one
                        if other_obj['color'] != obj_color and (r, c) in other_obj['coords']:
                            is_part_of_other_obj = True
                            break
                    if not is_part_of_other_obj:
                         counts_inside_others[pixel_color] = counts_inside_others.get(pixel_color, 0) + 1

    if counts_inside_others:
        # The color most frequently found *inside* other objects is likely the noise
        noise_color = max(counts_inside_others, key=counts_inside_others.get)
    else:
        # Fallback: most frequent color overall
        colors, counts = np.unique(grid, return_counts=True)
        # Exclude the color of the largest object if possible, as background is often most frequent
        largest_obj_color = -1
        if objects:
             objects.sort(key=lambda o: o['size'], reverse=True)
             largest_obj_color = objects[0]['color']
        
        sorted_indices = np.argsort(counts)[::-1]
        noise_color = colors[sorted_indices[0]]
        if noise_color == largest_obj_color and len(colors) > 1:
            # If most frequent is the largest object, pick the second most frequent
            if len(sorted_indices) > 1:
                 noise_color = colors[sorted_indices[1]]
            # If only one color besides largest, that must be it (or maybe grid is just one object?)
            # This fallback needs care, but the primary heuristic should work for the examples.

    return noise_color

# --- Main Transformation Function ---
def transform(input_grid):
    """
    Transforms the input grid by identifying target and source frames,
    filling noise in target frames using source frame colors, and
    reassembling the modified target frames.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Find all distinct objects
    all_objects = find_objects(grid)

    # 2. Determine the noise color
    if not all_objects: return grid.tolist() # Handle empty grid case
    noise_color = determine_noise_color(grid, all_objects)

    # 3. Filter out noise objects and get primary shapes
    shapes = [obj for obj in all_objects if obj['color'] != noise_color]
    if not shapes: return grid.tolist() # No non-noise shapes found

    # 4. Group shapes into Targets and Sources
    #    Heuristic: Divide spatially (e.g., top vs bottom half)
    #    Refinement: Identify target group (contains noise, or larger objects)
    shapes.sort(key=lambda o: (o['bbox'][0], o['bbox'][2])) # Sort by position
    
    targets = []
    sources = []
    
    # Try splitting by median row of shape origins
    median_row = np.median([s['bbox'][0] for s in shapes])
    group1 = [s for s in shapes if s['bbox'][0] < median_row]
    group2 = [s for s in shapes if s['bbox'][0] >= median_row]

    # If split is uneven, try simple first half / second half
    if len(group1) != len(group2) or not group1:
        mid_point = len(shapes) // 2
        group1 = shapes[:mid_point]
        group2 = shapes[mid_point:]
    
    if len(group1) != len(group2) or not group1:
         # Cannot form two equal groups, fallback or error
         # For this problem, examples suggest equal groups are expected.
         # If logic fails, returning original might be safest in ARC.
         # print("Warning: Could not divide shapes into two equal groups.")
         return grid.tolist() 

    # Determine which group is Target (contains noise within bbox)
    group1_has_noise = False
    for obj in group1:
        min_r, max_r, min_c, max_c = obj['bbox']
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if grid[r,c] == noise_color and (r,c) not in obj['coords']:
                     # Check if noise belongs to another non-noise shape within bbox? (Less strict here)
                     is_other_shape = False
                     for other in shapes:
                         if other != obj and (r,c) in other['coords']:
                             is_other_shape = True
                             break
                     if not is_other_shape:
                        group1_has_noise = True
                        break
            if group1_has_noise: break
    
    group2_has_noise = False
    for obj in group2:
        min_r, max_r, min_c, max_c = obj['bbox']
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                 if grid[r,c] == noise_color and (r,c) not in obj['coords']:
                     is_other_shape = False
                     for other in shapes:
                         if other != obj and (r,c) in other['coords']:
                             is_other_shape = True
                             break
                     if not is_other_shape:
                         group2_has_noise = True
                         break
            if group2_has_noise: break

    # Assign Target/Source based on noise presence
    if group1_has_noise and not group2_has_noise:
        targets = group1
        sources = group2
    elif group2_has_noise and not group1_has_noise:
        targets = group2
        sources = group1
    else: # Ambiguous case (both/neither have noise, or noise detection failed)
          # Use size heuristic (seen in Example 2 analysis)
          avg_size1 = sum(s['size'] for s in group1) / len(group1)
          avg_size2 = sum(s['size'] for s in group2) / len(group2)
          if avg_size1 >= avg_size2: # Default to group1 if equal
              targets = group1
              sources = group2
          else:
              targets = group2
              sources = group1

    # Ensure sorting within groups for consistent pairing
    targets.sort(key=lambda o: (o['bbox'][0], o['bbox'][2]))
    sources.sort(key=lambda o: (o['bbox'][0], o['bbox'][2]))

    # 5. Modify Target Frames
    modified_targets_data = []
    for target, source in zip(targets, sources):
        min_r, max_r, min_c, max_c = target['bbox']
        filler_color = source['color']

        # Extract subgrid based on target's bounding box
        subgrid = grid[min_r:max_r+1, min_c:max_c+1].copy()

        # Replace noise pixels within this subgrid
        subgrid[subgrid == noise_color] = filler_color

        modified_targets_data.append({
            'bbox': target['bbox'], # Store original bbox for layout
            'subgrid': subgrid
        })

    # 6. Assemble Output Grid
    if not modified_targets_data:
        return grid.tolist() # Should not happen if groups were found

    # Calculate relative positions and final grid size
    min_target_r = min(t['bbox'][0] for t in modified_targets_data)
    min_target_c = min(t['bbox'][2] for t in modified_targets_data)

    max_output_r = 0
    max_output_c = 0
    output_layout = []

    for data in modified_targets_data:
        bbox = data['bbox']
        subgrid = data['subgrid']
        h, w = subgrid.shape
        # Position relative to the top-leftmost target's origin
        rel_r = bbox[0] - min_target_r
        rel_c = bbox[2] - min_target_c

        output_layout.append({
            'rel_r': rel_r,
            'rel_c': rel_c,
            'subgrid': subgrid,
            'h': h,
            'w': w
        })
        # Update max dimensions needed
        max_output_r = max(max_output_r, rel_r + h)
        max_output_c = max(max_output_c, rel_c + w)

    # Create and populate the output grid
    # Initialize with 0 (white), assuming it's not a significant color in outputs
    output_grid = np.zeros((max_output_r, max_output_c), dtype=int)

    for layout_info in output_layout:
        r, c = layout_info['rel_r'], layout_info['rel_c']
        h, w = layout_info['h'], layout_info['w']
        subgrid = layout_info['subgrid']
        output_grid[r:r+h, c:c+w] = subgrid

    return output_grid.tolist()
```