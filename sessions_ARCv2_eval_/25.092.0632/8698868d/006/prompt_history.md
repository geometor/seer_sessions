
## train_1

**input:**
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


**output:**
```
1 1 1 1 1 1 4 4 4 4 4 4
1 2 2 2 2 1 4 3 3 3 3 4
1 2 1 1 2 1 4 3 3 4 3 4
1 2 1 1 2 1 4 3 4 3 3 4
1 2 2 2 2 1 4 3 3 3 3 4
1 1 1 1 1 1 4 4 4 4 4 4
```


## train_2

**input:**
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


**output:**
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

Okay, let's analyze the provided examples.

**Perception**

1.  **Input Structure:** The input grids contain multiple distinct, roughly rectangular blocks of solid color ("frames") separated by a background color. Within each frame, some pixels match the surrounding background color, appearing as "noise" or "holes".
2.  **Output Structure:** The output grids are smaller than the inputs and consist of reassembled versions of *some* of the input frames. The background color and some of the original frames are absent in the output.
3.  **Transformation Core:** The core transformation involves identifying the frames and the background/noise color. For a selected subset of frames (let's call them "target frames"), the internal noise pixels are replaced by colors derived from *other* frames in the input (let's call them "source frames").
4.  **Frame Selection and Pairing:** In both examples, the input frames seem divisible into two sets based on spatial arrangement (e.g., top half vs. bottom half, or first group vs. second group). One set acts as the target frames, whose structure is preserved in the output. The other set acts as the source frames, providing the colors to fill the noise in the target frames. The pairing between target and source frames appears based on their relative positions within their respective sets.
5.  **Color Replacement:** For each target frame, its internal noise pixels (pixels matching the background color within the frame's bounding box) are recolored using the solid color of its paired source frame.
6.  **Assembly:** The modified target frames are then assembled into the output grid, maintaining their relative spatial arrangement from the input.

**Facts**


```yaml
task_description: Identify distinct colored rectangular shapes (frames) separated by a background/noise color. Some frames contain noise pixels matching the background color. Identify a second set of frames. Pair frames from the first set (targets) with frames from the second set (sources) based on relative position. For each target frame, replace its internal noise pixels with the color of its paired source frame. Assemble the modified target frames to create the output grid.

example_1:
  input_grid_size: [20, 15]
  output_grid_size: [6, 12]
  background_noise_color: azure (8)
  target_frames:
    - color: blue (1)
      position: top-left
      size: [6, 6]
      internal_noise: yes
    - color: yellow (4)
      position: top-right
      size: [6, 6]
      internal_noise: yes
  source_frames:
    - color: red (2)
      position: middle-left (relative bottom-left)
      size: [4, 4]
    - color: green (3)
      position: middle-right (relative bottom-right)
      size: [4, 4]
  pairing:
    - target: blue (1)
      source_color: red (2) # from bottom-left source frame
    - target: yellow (4)
      source_color: green (3) # from bottom-right source frame
  action:
    - Replace azure (8) noise inside blue (1) frame with red (2).
    - Replace azure (8) noise inside yellow (4) frame with green (3).
  assembly:
    - Place modified blue frame on the left.
    - Place modified yellow frame on the right.
    - Resulting grid size: 6x12

example_2:
  input_grid_size: [30, 30]
  output_grid_size: [16, 16]
  background_noise_color: red (2)
  target_frames:
    - color: yellow (4)
      position: top-left (quadrant 1)
      size: [8, 8]
      internal_noise: yes
    - color: green (3)
      position: top-right (quadrant 2)
      size: [8, 8]
      internal_noise: yes
    - color: azure (8)
      position: middle-left (quadrant 3)
      size: [8, 8]
      internal_noise: yes
    - color: blue (1)
      position: middle-right (quadrant 4)
      size: [8, 8]
      internal_noise: yes
  source_frames: # Located within the red background area
    - color: maroon (9)
      position: relative top-left within noise area
    - color: orange (7)
      position: relative bottom-right within noise area
    - color: blue (1)
      position: relative bottom-left within noise area
    - color: gray (5)
      position: relative middle-right within noise area
  pairing: # Based on relative 2x2 positions
    - target: yellow (4) # top-left target
      source_color: maroon (9) # top-left source
    - target: green (3) # top-right target
      source_color: orange (7) # bottom-right source
    - target: azure (8) # middle-left target
      source_color: blue (1) # bottom-left source
    - target: blue (1) # middle-right target
      source_color: gray (5) # middle-right source
  action:
    - Replace red (2) noise inside yellow (4) frame with maroon (9).
    - Replace red (2) noise inside green (3) frame with orange (7).
    - Replace red (2) noise inside azure (8) frame with blue (1).
    - Replace red (2) noise inside blue (1) frame with gray (5).
  assembly:
    - Assemble modified frames in a 2x2 grid matching their original relative positions.
    - Resulting grid size: 16x16

```


**Natural Language Program**

1.  **Identify Noise Color:** Determine the primary background color that separates the main colored shapes and also appears as noise *inside* those shapes.
2.  **Segment Shapes:** Identify all distinct, contiguous colored shapes (frames) that are not the noise color. Record their primary color, bounding box, and relative position.
3.  **Group Shapes:** Divide the identified frames into two groups (Group A and Group B) based on their spatial layout (e.g., top half vs. bottom half, or first cluster vs. second cluster). Ensure both groups have the same number of frames and a similar relative spatial arrangement. Group A will be the 'target' frames used for the output structure, and Group B will be the 'source' frames providing filler colors.
4.  **Pair Shapes:** For each frame in Group A, find its corresponding frame in Group B based on their relative positions within their respective groups (e.g., top-left of Group A pairs with top-left of Group B, top-right with top-right, etc.).
5.  **Modify Target Frames:** For each frame in Group A:
    a.  Determine the color of its paired frame from Group B (`filler_color`).
    b.  Iterate through all pixels within the bounding box of the Group A frame.
    c.  If a pixel's color matches the `noise_color`, change its color to the `filler_color`.
6.  **Assemble Output:** Create a new grid by arranging the modified frames from Group A. Maintain the same relative spatial arrangement they had in the input grid. Discard the frames from Group B. The dimensions of the output grid will be determined by the combined dimensions of the modified Group A frames.
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
