
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 2 0 0 0 0 0 1 2 1 1 1 4 1
0 0 2 2 2 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 2 2 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 1 6 1 1 1 3 1
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 2 0 0 4 0
2 2 2 0 4 4 4
0 2 2 0 0 4 4
0 0 0 0 0 0 0
6 0 6 0 3 3 0
0 6 0 0 3 0 3
6 6 6 0 0 3 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 2 0 2 0 0 0
0 0 0 4 0 0 0 0 2 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0
1 4 1 1 1 8 1 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 8 0 0
1 1 1 1 1 1 1 0 0 8 0 8 0
1 1 1 1 1 1 1 0 0 0 8 0 0
1 3 1 1 1 2 1 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0
```


**output:**
```
0 4 0 0 0 8 0
4 4 4 0 8 0 8
0 4 0 0 0 8 0
0 0 0 0 0 0 0
3 0 3 0 2 2 0
3 3 0 0 2 0 2
0 3 0 0 0 2 0
```


## train_3

**input:**
```
1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 5 1 1 1 4 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 4 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 4 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 4 4 4 0 0 0 0
1 2 1 1 1 3 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 2 0 0 0 0 6 0 0
0 0 3 0 3 0 0 0 2 0 2 0 0 0 0 0 0
0 0 0 3 3 0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 5 0 0 0 0 0 8 8 8 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 0 0 0 0 4
5 5 0 0 0 4 0
0 0 5 0 4 4 4
0 0 0 0 0 0 0
0 2 0 0 3 0 3
2 0 2 0 0 3 3
2 2 2 0 0 0 3
```

*   **Perception of the elements:**
    *   The input grids contain multiple distinct objects (contiguous blocks of non-white pixels) on a white background.
    *   One prominent object is always composed of blue pixels (color 1). This blue object often forms a frame or a boundary, typically rectangular or L-shaped, near one edge or corner of the grid.
    *   Other objects are composed of various colors (red, green, yellow, gray, magenta, azure, maroon, orange).
    *   Some of these other colored objects appear inside or touching the area defined by the blue frame, while others are located distinctly separate from it.
    *   The output grid contains a subset of the non-blue objects from the input grid.
    *   The objects present in the output are those from the input that were *not* located inside or touching the blue frame.
    *   The relative positions of the kept objects are preserved in the output.
    *   The output grid is smaller than the input grid and seems sized to tightly fit the collection of kept objects.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - element: grid
        properties:
          - background_color: white (0)
          - contains: multiple objects
      - element: object
        properties:
          - type: blue_frame
            color: blue (1)
            shape: variable (often rectangular or L-shaped frame)
            role: boundary marker or filter region
          - type: colored_shape
            color: non-white (0), non-blue (1)
            shape: variable geometric forms
            role: content to be potentially filtered
    relationships:
      - type: spatial
        nodes: [colored_shape, blue_frame]
        property: adjacency (8-connectivity - sharing edge or corner)
        significance: Determines filtering; shapes adjacent to the blue_frame are excluded.
      - type: spatial
        nodes: [kept_colored_shapes] # Shapes not adjacent to blue_frame
        property: relative_position
        significance: Preserved between input and output.
    actions:
      - identify: all non-white objects
      - classify: objects into 'blue_frame' and 'colored_shape'
      - check: adjacency between each 'colored_shape' pixel and any 'blue_frame' pixel
      - filter: keep 'colored_shape' objects that have no adjacency to the 'blue_frame'
      - calculate: minimum bounding box containing all kept 'colored_shape' objects
      - construct: output grid based on bounding box size
      - place: kept 'colored_shape' objects into the output grid, maintaining relative positions
    ```


*   **Natural Language Program:**
    1.  Identify all distinct contiguous objects composed of non-white (0) pixels within the input grid.
    2.  Separate these objects into two categories: those composed entirely of blue (1) pixels (the "frame objects") and all other non-white objects (the "content objects").
    3.  Initialize an empty list to store the content objects that should be kept.
    4.  For each content object:
        a.  Iterate through all pixels belonging to this content object.
        b.  For each pixel, check its 8 neighbors (including diagonals).
        c.  If any neighbor belongs to any of the blue frame objects identified in step 2, mark this content object as "adjacent to frame" and stop checking for this object.
        d.  If, after checking all pixels of the content object, it has not been marked as "adjacent to frame", add it to the list of kept objects.
    5.  If no objects are kept, the output is empty or handled as per specific task rules (likely an empty grid or a minimal 1x1 white grid, though examples show non-empty outputs).
    6.  If objects are kept:
        a.  Determine the minimum bounding box (minimum row, maximum row, minimum column, maximum column) that encompasses all pixels of all the kept objects.
        b.  Calculate the height and width of this bounding box.
        c.  Create a new output grid with this calculated height and width, initialized with the white (0) background color.
        d.  For each kept object, copy its pixels into the new output grid, translating their coordinates so that their positions relative to the top-left corner of the bounding box are maintained. (Specifically, subtract the minimum row and minimum column of the bounding box from the original coordinates of each pixel before placing it in the output grid).
    7.  Return the newly constructed output grid.
```python
import numpy as np
from collections import deque

"""
Identify all distinct contiguous objects of non-white pixels in the input grid.
Separate objects into blue (color 1) "frame" objects and other non-white "content" objects.
Filter the content objects, keeping only those that are not adjacent (including diagonally) to any pixel of any frame object.
Determine the minimum bounding box enclosing all kept content objects.
Create an output grid sized to this bounding box.
Place the kept content objects into the output grid, preserving their relative positions based on the bounding box's top-left corner.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-white color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (color, set_of_coordinates).
              set_of_coordinates contains (row, col) tuples for pixels in the object.
    """
    height, width = grid.shape
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                if obj_coords: # Ensure we found something (should always be true here)
                     objects.append((color, obj_coords))

    return objects


def get_neighbors(r, c, height, width):
    """ Gets all 8 neighboring coordinates for a pixel. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Filters objects based on adjacency to blue objects and extracts them into a minimal bounding box.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. & 2. Identify all objects and separate frame/content
    all_objects = find_objects(grid)
    
    frame_objects = [obj for obj in all_objects if obj[0] == 1]
    content_objects = [obj for obj in all_objects if obj[0] > 1] # Colors 2-9

    # Create a set of all coordinates belonging to frame objects for quick lookup
    frame_pixels = set().union(*[coords for _, coords in frame_objects])

    # 3. & 4. Filter content objects: Keep those not adjacent to frame objects
    kept_objects = []
    for color, coords in content_objects:
        is_adjacent_to_frame = False
        for r, c in coords:
            # Check 8 neighbors of each pixel in the content object
            for nr, nc in get_neighbors(r, c, height, width):
                if (nr, nc) in frame_pixels:
                    is_adjacent_to_frame = True
                    break # No need to check other neighbors for this pixel
            if is_adjacent_to_frame:
                break # No need to check other pixels for this object
        
        if not is_adjacent_to_frame:
            kept_objects.append((color, coords))

    # 5. Handle the case where no objects are kept
    if not kept_objects:
        # Returning a 1x1 white grid seems a reasonable default for ARC if output must exist
        # However, the examples provided always have output objects. If test cases differ, adjust this.
         return [[0]] 

    # 6. Determine the bounding box for kept objects
    all_kept_pixels = set().union(*[coords for _, coords in kept_objects])
    
    # This check is technically redundant now due to the check above, but good practice
    if not all_kept_pixels:
         return [[0]] 

    min_row = min(r for r, c in all_kept_pixels)
    max_row = max(r for r, c in all_kept_pixels)
    min_col = min(c for r, c in all_kept_pixels)
    max_col = max(c for r, c in all_kept_pixels)

    # Calculate output grid dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1

    # Create and initialize the output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 7. Place kept objects into the output grid, translating coordinates
    for color, coords in kept_objects:
        for r, c in coords:
            # Translate coordinates relative to the bounding box's top-left corner
            out_r = r - min_row
            out_c = c - min_col
            output_grid[out_r, out_c] = color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```
