```python
import numpy as np
from collections import deque, defaultdict

"""
The transformation identifies a background/noise color and a set of N (where N is expected to be even) distinct, large 'primary' colored shapes. 
These primary shapes are divided into Target shapes (those containing the noise color within their bounding box) and potentially Source shapes (the remaining primary shapes).
If the number of Targets equals the number of non-Target primary shapes, they are paired based on spatial order (e.g., top-left Target with top-left Source).
If not (e.g., all primary shapes are Targets), Source colors are derived from smaller, non-primary, non-noise shapes/patterns found elsewhere in the grid, again paired spatially/ordered relative to the Targets.
The output is created by taking the bounding box area of each Target shape from the input, replacing only the pixels matching the noise color within that area with the corresponding Source color, and assembling these modified areas into a new grid, preserving the Targets' original relative spatial arrangement.
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
              'bbox' (min_r, max_r, min_c, max_c), 'size', and 'avg_pos' (average row, col). 
              Returns empty list if grid is empty.
    """
    if grid.size == 0:
        return []
        
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
                sum_r, sum_c = 0, 0

                while q:
                    row, col = q.popleft()
                    coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    sum_r += row
                    sum_c += col
                    
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                obj_size = len(coords)
                if obj_size > 0:
                    avg_r = sum_r / obj_size
                    avg_c = sum_c / obj_size
                    objects.append({
                        'color': int(color), # Convert color to int
                        'coords': coords, # Keep coords as set
                        'bbox': tuple(map(int, (min_r, max_r, min_c, max_c))), # Convert bbox to tuple of ints
                        'size': obj_size,
                        'avg_pos': (avg_r, avg_c) # Store average position
                    })
    return objects

# --- Helper Function: Determine Noise Color ---
def determine_noise_color(grid, primary_shapes):
    """
    Determines the noise/background color based on frequency within primary shape bounding boxes.

    Args:
        grid (np.array): The input grid.
        primary_shapes (list): List of primary shape objects.

    Returns:
        int: The determined noise color. Returns -1 if unable to determine.
    """
    if grid.size == 0 or not primary_shapes:
        return -1 

    counts_inside_primary_bboxes = defaultdict(int)
    primary_colors = set(obj['color'] for obj in primary_shapes)

    for obj in primary_shapes:
        min_r, max_r, min_c, max_c = obj['bbox']
        # Check pixels *within* the bounding box
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                 pixel_color = int(grid[r,c])
                 # Count only if the pixel is not part of ANY primary shape
                 is_part_of_any_primary = False
                 # A faster check: count only if pixel color is NOT one of the primary colors
                 if pixel_color not in primary_colors:
                      counts_inside_primary_bboxes[pixel_color] += 1
                 # More precise (slower): check coords of all primary shapes
                 # for p_shape in primary_shapes:
                 #     if (r, c) in p_shape['coords']:
                 #         is_part_of_any_primary = True
                 #         break
                 # if not is_part_of_any_primary:
                 #      counts_inside_primary_bboxes[pixel_color] += 1

    if counts_inside_primary_bboxes:
        # The color most frequently found *inside* primary bboxes (excluding primary colors) is likely the noise
        noise_color = max(counts_inside_primary_bboxes, key=counts_inside_primary_bboxes.get)
        return noise_color
    else:
        # Fallback: If no non-primary colors found inside, maybe noise is one of the primary colors? Unlikely for this task.
        # Or maybe the most frequent color overall?
        colors, counts = np.unique(grid, return_counts=True)
        if len(colors) > 0:
            # Exclude primary colors from consideration if possible
            valid_indices = [i for i, c in enumerate(colors) if c not in primary_colors]
            if valid_indices:
                filtered_counts = counts[valid_indices]
                filtered_colors = colors[valid_indices]
                if len(filtered_counts)>0:
                    return int(filtered_colors[np.argmax(filtered_counts)])
            # If only primary colors exist or fallback needed, return most frequent overall
            return int(colors[np.argmax(counts)])
        return -1 # Cannot determine

# --- Main Transformation Function ---
def transform(input_grid):
    """
    Transforms the input grid by identifying target and source frames,
    filling noise in target frames using source frame colors/derived colors, 
    and reassembling the modified target frames.
    """
    grid = np.array(input_grid, dtype=int)
    if grid.size == 0:
        return []

    # 1. Find all distinct objects
    all_objects = find_objects(grid)
    if not all_objects: 
        return grid.tolist() 

    # 2. Identify Primary Shapes (e.g., 4 largest non-background)
    # First, guess background color (most frequent overall) to exclude it
    colors, counts = np.unique(grid, return_counts=True)
    potential_bg_color = -1
    if len(colors) > 0:
        potential_bg_color = int(colors[np.argmax(counts)])
    
    # Filter out potential background and sort by size
    non_bg_objects = [obj for obj in all_objects if obj['color'] != potential_bg_color]
    non_bg_objects.sort(key=lambda o: o['size'], reverse=True)
    
    # Assume N=4 primary shapes based on examples
    num_primary = 4 
    if len(non_bg_objects) < num_primary:
         # Fallback: use all non-background objects if less than N found
         # Or maybe N should be the largest even number <= len(non_bg_objects)?
         num_primary = len(non_bg_objects) // 2 * 2 # Largest even number <= available
         if num_primary == 0 and len(non_bg_objects) > 0: # Handle case of 1 non-bg object
              primary_shapes = non_bg_objects[:1] # Take the single one? Problem spec implies pairs.
              # Let's return original if we can't get at least 2 primary shapes
              return grid.tolist()
         elif num_primary == 0:
              return grid.tolist() # No non-bg objects

    primary_shapes = non_bg_objects[:num_primary]
    primary_shapes.sort(key=lambda o: (o['bbox'][0], o['bbox'][2])) # Sort by position

    # 3. Identify Noise Color using primary shapes
    noise_color = determine_noise_color(grid, primary_shapes)
    if noise_color == -1: 
         return grid.tolist() # Failed to determine noise

    # Re-filter all objects, excluding the *confirmed* noise color
    all_non_noise_objects = [obj for obj in all_objects if obj['color'] != noise_color]
    
    # Re-identify primary shapes among all non-noise objects by matching color and bbox/position
    # This ensures we didn't accidentally filter them if noise was misidentified initially
    primary_shape_identifiers = set((o['color'], o['bbox']) for o in primary_shapes)
    current_primary_shapes = []
    other_non_noise_objects = []
    for obj in all_non_noise_objects:
        if (obj['color'], obj['bbox']) in primary_shape_identifiers:
            current_primary_shapes.append(obj)
        else:
            other_non_noise_objects.append(obj) # These will be source components in Case 2
            
    if len(current_primary_shapes) != num_primary:
        # This shouldn't happen if noise detection is okay, but indicates an issue.
        return grid.tolist()
        
    current_primary_shapes.sort(key=lambda o: (o['bbox'][0], o['bbox'][2])) # Ensure sorted

    # 4. Identify Target Shapes among primary shapes
    target_shapes = []
    non_target_primary_shapes = []
    for obj in current_primary_shapes:
        min_r, max_r, min_c, max_c = obj['bbox']
        has_noise_inside = False
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                # Check if pixel is noise AND not part of the object itself
                if grid[r, c] == noise_color and (r, c) not in obj['coords']:
                    # More careful check: ensure the noise isn't part of *another* primary shape
                    is_part_of_other_primary = False
                    for other_p in current_primary_shapes:
                         if other_p != obj and (r,c) in other_p['coords']:
                             is_part_of_other_primary = True
                             break
                    if not is_part_of_other_primary:
                         has_noise_inside = True
                         break
            if has_noise_inside:
                break
        if has_noise_inside:
            target_shapes.append(obj)
        else:
            non_target_primary_shapes.append(obj)

    target_shapes.sort(key=lambda o: (o['bbox'][0], o['bbox'][2]))
    non_target_primary_shapes.sort(key=lambda o: (o['bbox'][0], o['bbox'][2]))

    # 5. Determine Source Colors & Pairing
    paired_targets = [] # List of tuples: (target_obj, source_color)

    if len(target_shapes) == len(non_target_primary_shapes) and len(target_shapes) > 0:
        # Case 1: Pair targets with non-target primary shapes (like Ex 1)
        for i in range(len(target_shapes)):
            target = target_shapes[i]
            source = non_target_primary_shapes[i]
            paired_targets.append((target, source['color']))
    elif len(target_shapes) == num_primary and num_primary > 0:
        # Case 2: All primary shapes are targets (like Ex 2)
        # Source colors derived from 'other_non_noise_objects'
        
        source_components = other_non_noise_objects
        source_colors_data = defaultdict(list) # Store coords for each potential source color
        for comp in source_components:
            source_colors_data[comp['color']].extend(list(comp['coords']))
            
        unique_source_colors = sorted(list(source_colors_data.keys()))

        if len(unique_source_colors) == len(target_shapes):
            # Calculate average position for each source color
            avg_pos_by_color = {}
            for color, coords_list in source_colors_data.items():
                if coords_list:
                    avg_r = sum(r for r, c in coords_list) / len(coords_list)
                    avg_c = sum(c for r, c in coords_list) / len(coords_list)
                    avg_pos_by_color[color] = (avg_r, avg_c)
                else:
                     avg_pos_by_color[color] = (float('inf'), float('inf')) # Should not happen

            # Sort source colors based on their average position
            sorted_source_colors = sorted(unique_source_colors, key=lambda c: avg_pos_by_color[c])

            # Pair sorted targets with sorted source colors
            for i in range(len(target_shapes)):
                paired_targets.append((target_shapes[i], sorted_source_colors[i]))
        else:
            # Failed to find matching number of source colors
            return grid.tolist()
            
    else:
        # Ambiguous case or error in logic (e.g., odd number of targets/sources)
        return grid.tolist()

    # 6. Modify Target Shapes
    modified_targets_data = []
    for target, source_color in paired_targets:
        min_r, max_r, min_c, max_c = target['bbox']
        
        # Extract subgrid based on target's bounding box from the *original* grid
        subgrid_original = grid[min_r:max_r+1, min_c:max_c+1]
        modified_subgrid = subgrid_original.copy()

        # Replace ONLY noise pixels within this subgrid copy
        noise_mask = (modified_subgrid == noise_color)
        modified_subgrid[noise_mask] = source_color

        modified_targets_data.append({
            'bbox': target['bbox'], # Store original bbox for layout calculation
            'subgrid': modified_subgrid
        })

    # 7. Assemble Output Grid
    if not modified_targets_data:
        return grid.tolist() 

    # Calculate relative positions and final grid size based on target bboxes
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
            'rel_r': rel_r, 'rel_c': rel_c, 'subgrid': subgrid, 'h': h, 'w': w
        })
        # Update max dimensions needed
        max_output_r = max(max_output_r, rel_r + h)
        max_output_c = max(max_output_c, rel_c + w)

    # Create and populate the output grid. Initialize with 0 (white).
    output_grid = np.zeros((max_output_r, max_output_c), dtype=int) 

    for layout_info in output_layout:
        r, c = layout_info['rel_r'], layout_info['rel_c']
        h, w = layout_info['h'], layout_info['w']
        subgrid = layout_info['subgrid']
        # Place the modified subgrid onto the output grid
        output_grid[r:r+h, c:c+w] = subgrid

    return output_grid.tolist()
```