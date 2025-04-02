
## train_1

**input:**
```
2 2 2 2 2 0 0 0
2 0 3 3 2 3 3 0
2 0 3 3 2 3 3 0
2 0 3 3 2 3 3 0
2 2 2 2 2 3 3 0
0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2 0 0 0
2 0 3 3 3 3 3 0
2 0 3 3 3 3 3 0
2 0 3 3 3 3 3 0
2 2 3 3 3 3 3 0
0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 6 6 6 6
0 0 7 7 7 7 7 6
0 0 7 0 6 6 7 6
0 0 7 7 7 7 7 6
0 0 0 0 6 6 6 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 6 6 6 6
0 0 7 7 6 6 6 6
0 0 7 0 6 6 6 6
0 0 7 7 6 6 6 6
0 0 0 0 6 6 6 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation.

### Perception

1.  **Grid Structure:** Both examples operate on 8x8 grids. The background color is consistently white (0).
2.  **Key Objects:** In both inputs, there are two primary non-background objects:
    *   A larger object that forms a kind of 'U' shape or frame, open on one side (left in example 1, top in example 2). Let's call this the "Frame Object".
    *   One or more other distinct objects located partially inside or adjacent to the opening/cavity of the Frame Object. Let's call these "Inner Objects".
3.  **Interaction:** The transformation clearly involves an interaction between the Frame Object and the Inner Object(s) where they are adjacent or nearly adjacent. The output grid shows modifications primarily at the boundary between these objects.
4.  **Color Dependency:** The nature of the modification seems to depend crucially on the color of the Inner Object.
    *   In `train_1`, the Frame is Red(2) and the Inner Object is Green(3). The output shows some pixels of the *Frame* changing color to match the *Inner* object (Red -> Green).
    *   In `train_2`, the Frame is Magenta(6) and the Inner Object is Orange(7). The output shows some pixels of the *Inner* object changing color to match the *Frame* (Orange -> Magenta).
5.  **Specific Rule Trigger:** The presence of Green(3) as the Inner Object color in `train_1` appears to trigger a different rule ("Frame pixels change") compared to `train_2` where the Inner Object color is Orange(7) ("Inner pixels change"). The specific color Green(3) seems to be the deciding factor.
6.  **Adjacency:** The changes occur only where pixels of the Frame Object and Inner Object(s) are adjacent (sharing a side, i.e., 4-connectivity).

### Facts


```yaml
task_context:
  grid_size: ثابت (8x8 in examples)
  background_color: white (0)
  num_examples: 2

identified_objects:
  - object_type: Frame
    description: A large, often U-shaped or enclosing object.
    properties:
      - color: (Red(2) in ex1, Magenta(6) in ex2)
      - forms_boundary: True
  - object_type: InnerObject
    description: An object adjacent to the Frame, often partially within its concave area.
    properties:
      - color: (Green(3) in ex1, Orange(7) in ex2)
      - position: Adjacent to Frame object
      - count: Can be one or more parts (ex1 has two green parts, ex2 has one orange part)

relationships:
  - type: Adjacency
    description: Pixels of the Frame object are adjacent (4-connectivity) to pixels of the InnerObject. This adjacency is the site of interaction.

transformation_properties:
  - type: Conditional Color Change
    description: The color change rule depends on the color of the InnerObject.
    condition: InnerObject color == Green(3)
    rule_if_true: Certain Frame pixels adjacent to the InnerObject change color to Green(3).
    rule_if_false: Certain InnerObject pixels adjacent to the Frame change color to the Frame's color.
  - type: Locality
    description: Changes only occur at or near the boundary pixels involved in the adjacency relationship.
  - type: Frame Integrity (Partial)
    description: The Frame object mostly retains its shape and color, except when the InnerObject is Green(3).
  - type: Inner Object Integrity (Partial)
    description: The InnerObject mostly retains its shape and color, except when it's not Green(3) and adjacent to the Frame.

example_specific_details:
  - example: train_1
    frame_color: Red(2)
    inner_color: Green(3)
    action: Change adjacent Frame pixels (Red 2) to Inner color (Green 3).
    affected_pixels: Specific pixels on the 'bottom' edge of the U-frame change.
  - example: train_2
    frame_color: Magenta(6)
    inner_color: Orange(7)
    action: Change adjacent Inner pixels (Orange 7) to Frame color (Magenta 6).
    affected_pixels: Specific Orange pixels touching the Magenta frame change.

```


### Natural Language Program

1.  Identify the background color (assume white 0).
2.  Identify all contiguous non-background objects.
3.  Designate the object that forms a partial enclosure or 'U' shape as the "Frame Object". Record its color (`C_frame`).
4.  Identify any other distinct non-background object(s) adjacent (sharing a side, 4-connectivity) to the Frame Object as "Inner Objects". Determine the set of colors (`S_inner`) present in these Inner Objects.
5.  Check if the color Green(3) is present in `S_inner`.
6.  **If Green(3) is in `S_inner`:**
    *   Iterate through each pixel `P_frame` belonging to the Frame Object.
    *   Check if `P_frame` is adjacent (4-connectivity) to *any* pixel `P_inner` belonging to an Inner Object whose color is Green(3).
    *   If such adjacency exists, change the color of `P_frame` in the output grid to Green(3).
    *   Keep all other pixels (non-adjacent frame pixels, inner object pixels, background pixels) unchanged from the input grid.
7.  **If Green(3) is NOT in `S_inner`:**
    *   Iterate through each pixel `P_inner` belonging to any Inner Object.
    *   Check if `P_inner` is adjacent (4-connectivity) to *any* pixel `P_frame` belonging to the Frame Object.
    *   If such adjacency exists, change the color of `P_inner` in the output grid to `C_frame` (the color of the Frame Object).
    *   Keep all other pixels (non-adjacent inner object pixels, frame object pixels
```python
import numpy as np
from collections import deque

"""
Identifies objects in the grid based on color contiguity.
Determines a "Frame" object, often U-shaped or partially enclosing others, potentially by identifying the non-background object whose bounding box touches the most grid edges.
Identifies "Inner" objects adjacent to the Frame.
Applies a transformation based on the color of the Inner objects:
1. If any Inner object has the color Green (3), adjacent pixels of the Frame object change their color to Green (3).
2. If no Inner object is Green (3), adjacent pixels of the Inner objects change their color to match the Frame object's color.
The background color is assumed to be White (0). Adjacency is defined by 4-connectivity (sharing a side).
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'coords' (set of tuples (r, c)).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0 # Assuming white is background

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color and not visited[r, c]:
                # Start BFS to find the extent of this object
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 4 neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            obj_coords.add((nr, nc))
                
                objects.append({'color': color, 'coords': obj_coords})
    return objects

def get_bounding_box(coords):
    """ Calculates min/max row/col from a set of coordinates """
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return (min_r, min_c, max_r, max_c)

def count_touching_edges(bbox, grid_height, grid_width):
    """ Counts how many grid edges the bbox touches """
    if bbox is None:
        return 0
    min_r, min_c, max_r, max_c = bbox
    count = 0
    if min_r == 0: count += 1
    if max_r == grid_height - 1: count += 1
    if min_c == 0: count += 1
    if max_c == grid_width - 1: count += 1
    return count

def transform(input_grid):
    """
    Applies the transformation rule based on object adjacency and color rules.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    background_color = 0
    green_color = 3

    # 1. Find all non-background objects
    objects = find_objects(input_np)
    if not objects:
        return output_grid.tolist() # No objects to transform

    # 2. Identify Frame and Inner objects
    frame_object = None
    inner_objects = []
    
    # Heuristic: Frame is the object touching the most grid edges
    max_edges = -1
    for obj in objects:
        bbox = get_bounding_box(obj['coords'])
        edges = count_touching_edges(bbox, height, width)
        if edges > max_edges:
            max_edges = edges
            frame_object = obj
        elif edges == max_edges:
             # Ambiguity: If multiple objects touch the same max number of edges,
             # this heuristic might fail. We might need a tie-breaker (e.g., largest area?).
             # For now, arbitrarily pick the first one found with max edges.
             # A more robust solution might be needed if tie-breaking is important.
             pass 

    if frame_object is None:
        # Fallback or error handling if no clear frame is found
        # For now, assume the largest object if edge heuristic fails?
        if objects:
           frame_object = max(objects, key=lambda o: len(o['coords']))
        else: # Should not happen if objects is not empty, but defensive check
           return output_grid.tolist()


    frame_color = frame_object['color']
    frame_coords = frame_object['coords']
    inner_colors = set()
    inner_coords_map = {} # Map color to set of coordinates

    for obj in objects:
        if obj != frame_object:
            inner_objects.append(obj)
            inner_colors.add(obj['color'])
            if obj['color'] not in inner_coords_map:
                inner_coords_map[obj['color']] = set()
            inner_coords_map[obj['color']].update(obj['coords'])

    # 3. Check if Green (3) is among inner colors
    green_is_inner = green_color in inner_colors

    # 4. Apply transformation rule
    if green_is_inner:
        # Rule 1: Change adjacent Frame pixels to Green
        for r, c in frame_coords:
            # Check 4 neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Check if neighbor is within grid bounds and is Green
                if 0 <= nr < height and 0 <= nc < width and input_np[nr, nc] == green_color:
                    # Check if the green neighbor belongs to an *inner* object
                    # (This check prevents green frame pixels changing adjacent frame pixels)
                    if (nr, nc) in inner_coords_map.get(green_color, set()):
                       output_grid[r, c] = green_color
                       break # Change the frame pixel and move to the next frame pixel
    
    else:
        # Rule 2: Change adjacent Inner pixels to Frame color
        for inner_obj in inner_objects:
            inner_color = inner_obj['color']
            for r, c in inner_obj['coords']:
                 # Check 4 neighbors
                 for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                     nr, nc = r + dr, c + dc
                     # Check if neighbor is within grid bounds and is the Frame color
                     if 0 <= nr < height and 0 <= nc < width and input_np[nr, nc] == frame_color:
                        # Check if the frame-colored neighbor actually belongs to the identified frame object
                         if (nr, nc) in frame_coords:
                            output_grid[r, c] = frame_color
                            break # Change the inner pixel and move to the next inner pixel


    return output_grid.tolist()
```
