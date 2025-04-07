```python
import numpy as np
from collections import deque

"""
Identify distinct colored rectangular shapes (frames) separated by a background/noise color. 
Some frames contain noise pixels matching the background color. Identify a second set of frames. 
Pair frames from the first set (targets) with frames from the second set (sources) based on relative position. 
For each target frame, replace its internal noise pixels with the color of its paired source frame. 
Assemble the modified target frames, maintaining their original relative spatial arrangement, to create the output grid.

Workflow:
1. Find all distinct contiguous objects (non-background shapes) in the input grid.
2. Determine the background/noise color (heuristically, often the most frequent color, or the color separating major objects).
3. Categorize objects into 'targets' (those containing the noise color within their bounding box) and 'sources' (those that don't).
4. Sort targets and sources based on their top-left corner positions (row, then column) to establish pairing.
5. For each target-source pair:
    a. Extract the target object's subgrid based on its bounding box.
    b. Create a copy of the subgrid.
    c. Replace all pixels matching the noise color within this copied subgrid with the source object's color.
    d. Store the modified subgrid and its original relative position.
6. Determine the layout and dimensions of the output grid based on the relative positions and sizes of the (modified) target subgrids.
7. Assemble the modified target subgrids into the final output grid.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid.
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color', 'coords' (set of (r, c) tuples), and 
              'bbox' (min_r, max_r, min_c, max_c).
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
                            
                if len(coords) > 0: # Avoid adding empty objects if logic allows
                     objects.append({
                         'color': color, 
                         'coords': coords, 
                         'bbox': (min_r, max_r, min_c, max_c)
                     })
    return objects

def determine_noise_color(grid, objects):
    """
    Determines the noise/background color.
    Heuristic: The most frequent color overall might be the noise, 
               especially if it's not the color of the largest objects or 
               appears inside other objects' bounding boxes.
               A simpler start: Assume the most frequent color is noise.
    """
    colors, counts = np.unique(grid, return_counts=True)
    # Exclude colors that form the main structure (optional, might need refinement)
    # Simple approach: most frequent color is noise
    noise_color = colors[np.argmax(counts)]
    
    # Refinement: Check if the most frequent color appears inside bounding boxes of other colors
    counts_inside_others = {}
    for obj in objects:
        min_r, max_r, min_c, max_c = obj['bbox']
        obj_color = obj['color']
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                pixel_color = grid[r, c]
                if pixel_color != obj_color:
                    counts_inside_others[pixel_color] = counts_inside_others.get(pixel_color, 0) + 1

    if counts_inside_others:
         # The color most frequently found *inside* other objects is likely the noise
         noise_color = max(counts_inside_others, key=counts_inside_others.get)
         # print(f"Noise color detected as {noise_color} based on presence inside other objects.")

    else: 
         # Fallback to most frequent overall if no color is found inside others
         noise_color = colors[np.argmax(counts)]
         # print(f"Noise color defaulted to most frequent overall: {noise_color}")

    return noise_color


def transform(input_grid):
    """
    Transforms the input grid based on the described logic.
    """
    grid = np.array(input_grid, dtype=int)
    
    # 1. Find all objects
    all_objects = find_objects(grid)

    # 2. Determine noise color
    noise_color = determine_noise_color(grid, all_objects)
    
    # Filter out objects that are just noise color
    objects = [obj for obj in all_objects if obj['color'] != noise_color]

    # 3. Categorize objects into targets and sources
    targets = []
    sources = []
    for obj in objects:
        min_r, max_r, min_c, max_c = obj['bbox']
        has_noise_inside = False
        # Check only within the bounding box, not the exact object coords
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                 # Check if the point is within the bounding box AND is noise color
                 # AND is not part of the object itself (though noise shouldn't be)
                if grid[r, c] == noise_color:
                     # A simple check is enough: is noise present in the bbox?
                     # More precise: is noise present at a coordinate *not* belonging to the object?
                     # Even simpler for now: If ANY noise is in the bbox, it's a potential target.
                     has_noise_inside = True
                     break
            if has_noise_inside:
                break
                
        if has_noise_inside:
            targets.append(obj)
        else:
            sources.append(obj)

    # Handle cases where categorization might be imperfect (e.g., noise object itself)
    # Ensure targets are generally larger than sources if ambiguity exists? (Not implemented here)
    
    # 4. Sort targets and sources by position (top-left corner)
    targets.sort(key=lambda o: (o['bbox'][0], o['bbox'][2]))
    sources.sort(key=lambda o: (o['bbox'][0], o['bbox'][2]))

    if not targets or len(targets) != len(sources):
        # If grouping/pairing fails, return original or empty? 
        # Based on examples, we expect pairs. Return empty if assumption fails.
        print(f"Warning: Could not find equal number of targets ({len(targets)}) and sources ({len(sources)}).")
        # For ARC, returning the input might be safer if rules are uncertain. Let's return input.
        # Consider edge cases or alternative grouping if this occurs often.
        # return np.array([[]], dtype=int) 
        return grid # Return input if logic fails

    # 5. Modify target frames
    modified_targets_data = []
    for target, source in zip(targets, sources):
        min_r, max_r, min_c, max_c = target['bbox']
        filler_color = source['color']
        
        # Extract subgrid
        subgrid = grid[min_r:max_r+1, min_c:max_c+1]
        modified_subgrid = subgrid.copy()
        
        # Replace noise with filler color
        modified_subgrid[modified_subgrid == noise_color] = filler_color
        
        modified_targets_data.append({
            'bbox': target['bbox'],
            'subgrid': modified_subgrid
        })

    # 6. Determine output grid layout and dimensions
    if not modified_targets_data:
        return np.array([[]], dtype=int) # Should not happen if checks above passed

    # Find overall bounds and relative positions
    min_target_r = min(t['bbox'][0] for t in modified_targets_data)
    min_target_c = min(t['bbox'][2] for t in modified_targets_data)
    
    max_output_r = 0
    max_output_c = 0
    
    output_layout = []
    
    for data in modified_targets_data:
        bbox = data['bbox']
        subgrid = data['subgrid']
        h, w = subgrid.shape
        # Calculate position relative to the top-leftmost target's origin
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

    # 7. Assemble output grid
    # Initialize with a common background color? Or just fit the shapes?
    # The examples suggest the output has no external background, just the assembled shapes.
    # Use a temporary distinct color like -1 for initialization if needed, or infer background.
    # Let's use 0 (white) as a default background for assembly, assuming it's not a primary color.
    # A safer bet might be to use the noise color? No, output doesn't contain it. Use 0.
    output_grid = np.zeros((max_output_r, max_output_c), dtype=int) 

    for layout_info in output_layout:
        r, c = layout_info['rel_r'], layout_info['rel_c']
        h, w = layout_info['h'], layout_info['w']
        subgrid = layout_info['subgrid']
        output_grid[r:r+h, c:c+w] = subgrid
        
    return output_grid.tolist() # Return as list of lists per ARC format
```