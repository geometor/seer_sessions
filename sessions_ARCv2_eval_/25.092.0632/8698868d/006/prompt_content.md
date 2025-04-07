
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identify distinct colored shapes (frames) separated by a background/noise color. 
Group these frames into two equal sets based on spatial arrangement (e.g., top half vs. bottom half after sorting). 
Designate one set as 'Targets' and the other as 'Sources'. The Target set is typically the one whose frames contain pixels of the noise color within their bounding boxes.
Pair Target frames with Source frames based on their relative order within their respective groups (e.g., first Target with first Source, etc.). 
For each Target frame, create a modified version by taking its bounding box area from the input grid and replacing only the pixels matching the noise color with the solid color of its paired Source frame. 
Assemble these modified Target frames into the output grid, preserving their original relative spatial arrangement.
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
              'bbox' (min_r, max_r, min_c, max_c), and 'size'. Returns empty list if grid is empty.
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
    Primary heuristic: The color most frequently appearing *inside* the bounding boxes 
                      of other major objects, but not part of the object itself.
    Fallback heuristic: The most frequent color overall, excluding the color of the largest object.

    Args:
        grid (np.array): The input grid.
        objects (list): List of objects found by find_objects.

    Returns:
        int: The determined noise color. Returns -1 if unable to determine (e.g., empty grid).
    """
    if grid.size == 0 or not objects:
        return -1 

    counts_inside_others = {}
    # Consider objects larger than a small threshold to avoid noise pixels forming tiny 'objects'
    significant_objects = [obj for obj in objects if obj['size'] > 2] 
    if not significant_objects: # If only tiny objects, fallback might be needed
        significant_objects = objects # Use all if no large ones

    for obj in significant_objects:
        min_r, max_r, min_c, max_c = obj['bbox']
        obj_color = obj['color']
        # Check pixels *within* bbox but *not* part of the object itself
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if (r, c) not in obj['coords']:
                    pixel_color = grid[r, c]
                    # Ensure this 'inside' pixel isn't part of another significant object
                    is_part_of_other_sig_obj = False
                    for other_obj in significant_objects:
                        if other_obj != obj and (r, c) in other_obj['coords']:
                            is_part_of_other_sig_obj = True
                            break
                    if not is_part_of_other_sig_obj:
                         counts_inside_others[pixel_color] = counts_inside_others.get(pixel_color, 0) + 1

    if counts_inside_others:
        # The color most frequently found *inside* other objects is likely the noise
        noise_color = max(counts_inside_others, key=counts_inside_others.get)
        # print(f"Noise color identified as {noise_color} via 'inside' heuristic.")
        return noise_color
    else:
        # Fallback: most frequent color overall, trying to exclude the largest object's color
        colors, counts = np.unique(grid, return_counts=True)
        
        largest_obj_color = -1
        if objects:
             # Sort by size to find the largest object
             sorted_objects = sorted(objects, key=lambda o: o['size'], reverse=True)
             if sorted_objects:
                 largest_obj_color = sorted_objects[0]['color']
        
        sorted_indices = np.argsort(counts)[::-1]
        
        # Iterate through frequencies, pick the first one that isn't the largest object's color
        for idx in sorted_indices:
            potential_noise_color = colors[idx]
            if potential_noise_color != largest_obj_color:
                # print(f"Noise color identified as {potential_noise_color} via fallback heuristic (most frequent excluding largest).")
                return potential_noise_color
        
        # If all colors belong to the largest object or only one color exists
        if len(sorted_indices) > 0:
            # print(f"Noise color defaulted to most frequent overall: {colors[sorted_indices[0]]}.")
            return colors[sorted_indices[0]] # Return most frequent if exclusion failed
        else:
            return -1 # Should not happen if grid is not empty


# --- Main Transformation Function ---
def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    grid = np.array(input_grid, dtype=int)
    if grid.size == 0:
        return []

    # 1. Find all distinct objects
    all_objects = find_objects(grid)
    if not all_objects: 
        return grid.tolist() # Return original if no objects found

    # 2. Determine the noise color
    noise_color = determine_noise_color(grid, all_objects)
    if noise_color == -1: # If noise color couldn't be determined
         return grid.tolist() 

    # 3. Filter out noise objects and get primary shapes
    shapes = [obj for obj in all_objects if obj['color'] != noise_color]
    if not shapes or len(shapes) % 2 != 0: # Need an even number of shapes for pairing
        # print(f"Warning: Found {len(shapes)} non-noise shapes. Cannot form pairs.")
        return grid.tolist() 

    # 4. Group shapes into two equal sets based on spatial order
    shapes.sort(key=lambda o: (o['bbox'][0], o['bbox'][2])) # Sort primarily by row, then column
    mid_point = len(shapes) // 2
    group1 = shapes[:mid_point]
    group2 = shapes[mid_point:]

    # 5. Identify Target group (likely contains noise within bounding boxes)
    #    Check if any shape in group1 has noise inside its bbox (but not part of itself)
    group1_is_target = False
    for obj in group1:
        min_r, max_r, min_c, max_c = obj['bbox']
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if grid[r, c] == noise_color and (r, c) not in obj['coords']:
                    # Check if this noise pixel belongs to another non-noise shape in the grid
                    part_of_other_shape = False
                    for other_shape in shapes:
                         if other_shape != obj and (r,c) in other_shape['coords']:
                             part_of_other_shape = True
                             break
                    if not part_of_other_shape:
                         group1_is_target = True
                         break # Found noise belonging to the background within this bbox
            if group1_is_target: break
    
    if group1_is_target:
        targets = group1
        sources = group2
    else:
        # Assume group2 must be the target if group1 isn't (based on problem structure)
        # Could add a similar check for group2 for robustness, but let's assume complementarity
        targets = group2
        sources = group1
        
    # Ensure sorting within groups remains consistent for pairing
    targets.sort(key=lambda o: (o['bbox'][0], o['bbox'][2]))
    sources.sort(key=lambda o: (o['bbox'][0], o['bbox'][2]))

    # 6. Modify Target Frames by replacing noise with corresponding source color
    modified_targets_data = []
    for i in range(len(targets)):
        target = targets[i]
        # Handle potential index error if source group is smaller (shouldn't happen with checks)
        if i >= len(sources): 
             # print(f"Warning: Mismatch in target/source count during pairing.")
             continue # Skip this target if no corresponding source
        source = sources[i]
        
        min_r, max_r, min_c, max_c = target['bbox']
        filler_color = source['color']

        # Extract subgrid based on target's bounding box from the *original* grid
        subgrid_original = grid[min_r:max_r+1, min_c:max_c+1]
        modified_subgrid = subgrid_original.copy()

        # Replace ONLY noise pixels within this subgrid copy
        noise_mask = (modified_subgrid == noise_color)
        modified_subgrid[noise_mask] = filler_color

        modified_targets_data.append({
            'bbox': target['bbox'], # Store original bbox for layout calculation
            'subgrid': modified_subgrid
        })

    # 7. Assemble Output Grid using modified target subgrids
    if not modified_targets_data:
        # print("Warning: No modified target data generated.")
        return grid.tolist() # Return original if modification failed

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
            'rel_r': rel_r,
            'rel_c': rel_c,
            'subgrid': subgrid,
            'h': h,
            'w': w
        })
        # Update max dimensions needed for the output grid
        max_output_r = max(max_output_r, rel_r + h)
        max_output_c = max(max_output_c, rel_c + w)

    # Create and populate the output grid. Initialize with a neutral color (e.g., 0=white)
    # This assumes 0 is not a critical part of the final patterns themselves.
    # A safer but more complex init might involve analyzing output colors.
    output_grid = np.zeros((max_output_r, max_output_c), dtype=int) 

    for layout_info in output_layout:
        r, c = layout_info['rel_r'], layout_info['rel_c']
        h, w = layout_info['h'], layout_info['w']
        subgrid = layout_info['subgrid']
        # Place the modified subgrid onto the output grid
        output_grid[r:r+h, c:c+w] = subgrid

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
1 1 1 1 1 1 4 8 4 4 4 4 8 8 8
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
1 1 1 1 8 1 4 4 4 4 8 4 8 8 8
1 1 1 1 1 1 4 4 4 4 4 4 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 2 8 8 2 8 8 8 8 8 8 8 8 8
8 8 2 8 8 2 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
8 8 8 8 8 8 8 3 3 8 3 8 8 8 8
8 8 8 8 8 8 8 3 8 3 3 8 8 8 8
8 8 8 8 8 8 8 3 3 3 3 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
1 1 1 1 1 1 4 4 4 4 4 4
1 2 2 2 2 1 4 3 3 3 3 4
1 2 1 1 2 1 4 3 3 4 3 4
1 2 1 1 2 1 4 3 4 3 3 4
1 2 2 2 2 1 4 3 3 3 3 4
1 1 1 1 1 1 4 4 4 4 4 4
```
Transformed Output:
```
1 1 1 1 1 1 4 4 4 4 4 4
1 1 1 1 1 1 4 3 4 4 4 4
1 1 1 1 1 1 4 4 4 4 4 4
1 1 1 1 1 1 4 4 4 4 4 4
1 1 1 1 2 1 4 4 4 4 3 4
1 1 1 1 1 1 4 4 4 4 4 4
```
Match: False
Pixels Off: 23
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 63.888888888888886

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 2 2 2
4 4 2 4 4 2 4 4 3 3 3 3 3 2 3 3 2 2 2 9 9 9 9 9 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 2 2 9 2 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 2 2 9 2 9 2 2 2 2 2
4 4 2 4 4 4 4 4 3 3 2 3 3 3 3 3 2 2 2 9 9 9 9 2 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 2 2 9 2 9 2 2 2 2 2
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 2 2 2 9 9 9 9 9 9 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 2 8 8 1 1 2 1 1 2 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 2 1 1 2 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 5 5 5 5 5 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 2 2 5 2 5 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 2 2 5 2 5 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 5 5 5 5 5 5 2 2 2 2 2
2 2 2 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 5 2 2 5 2 5 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2 5 5 5 5 5 5 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 2 2 2 2 1 2 2 2 2 7 2 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 1 1 1 1 1 1 2 2 2 2 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 7 2 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 7 2 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```
Expected Output:
```
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3
4 9 9 9 9 9 9 4 3 7 7 7 7 7 7 3
4 9 4 4 9 4 9 4 3 7 3 7 7 7 7 3
4 9 4 4 9 4 9 4 3 7 7 7 7 7 7 3
4 9 9 9 9 4 9 4 3 7 3 7 7 7 7 3
4 9 4 4 9 4 9 4 3 7 3 7 7 7 7 3
4 9 9 9 9 9 9 4 3 7 7 7 7 7 7 3
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1
8 1 1 1 1 1 1 8 1 5 5 5 5 5 5 1
8 1 8 8 8 8 1 8 1 5 1 1 5 1 5 1
8 1 8 8 8 8 1 8 1 5 1 1 5 1 5 1
8 1 8 8 8 8 1 8 1 5 5 5 5 5 5 1
8 1 8 8 8 8 1 8 1 5 1 1 5 1 5 1
8 1 1 1 1 1 1 8 1 5 5 5 5 5 5 1
8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1
```
Transformed Output:
```
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
4 4 1 4 4 1 4 4 3 3 3 3 3 5 3 3 0 0 0 9 9 9 9 9 9
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 0 0 0 9 1 1 9 1 9
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 0 0 0 9 1 1 9 1 9
4 4 1 4 4 4 4 4 3 3 5 3 3 3 3 3 0 0 0 9 9 9 9 1 9
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 0 0 0 9 1 1 9 1 9
4 4 4 4 4 4 4 4 3 3 3 3 3 3 3 3 0 0 0 9 9 9 9 9 9
8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 7 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None
