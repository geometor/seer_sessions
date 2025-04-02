
## train_1

**input:**
```
0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 4 4 4 4 0 0 0 5 5 5 5 5 0
0 4 0 0 4 0 0 0 5 5 5 5 5 0
0 4 0 0 4 0 0 0 5 5 5 5 5 0
0 4 4 4 4 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0
0 3 3 3 0 0 4 4 4 4 0 0 0 0
0 3 0 3 0 0 4 4 4 4 0 0 0 0
0 3 3 3 0 0 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 4 4 4 4 0 0 0 5 0 0 0 5 0
0 4 4 4 4 0 0 0 5 0 0 0 5 0
0 4 4 4 4 0 0 0 5 0 0 0 5 0
0 4 4 4 4 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0
0 3 3 3 0 0 4 0 0 4 0 0 0 0
0 3 3 3 0 0 4 0 0 4 0 0 0 0
0 3 3 3 0 0 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The input grid contains four distinct objects on a white background: a yellow 'U' shape, a solid gray square, a green 'C' shape, and a solid yellow square. The output grid shows that the solid squares (gray and yellow) have been hollowed out, meaning their interior pixels have been changed to the background color (white), while their borders remain intact. The non-solid shapes (yellow 'U' and green 'C') are unchanged. The transformation rule appears to be: identify solid rectangular or square objects and make them hollow by changing their internal pixels to the background color.

*   **YAML Facts:**
    
```yaml
    background_color: 0 # white
    objects:
      - object_1:
          color: 4 # yellow
          shape: U-shape
          location: top-left quadrant
          bounding_box: rows 1-4, cols 1-4
          is_solid_rectangle: false
          action: unchanged
      - object_2:
          color: 5 # gray
          shape: square
          location: top-right quadrant
          bounding_box: rows 0-4, cols 8-12
          is_solid_rectangle: true
          action: hollow_out
          hollow_color: 0 # white
      - object_3:
          color: 3 # green
          shape: C-shape
          location: bottom-left quadrant
          bounding_box: rows 7-9, cols 1-3
          is_solid_rectangle: false
          action: unchanged
      - object_4:
          color: 4 # yellow
          shape: square
          location: bottom-center
          bounding_box: rows 6-9, cols 6-9
          is_solid_rectangle: true
          action: hollow_out
          hollow_color: 0 # white
    transformation_rule:
      - Identify contiguous non-background color objects.
      - For each object, determine its bounding box.
      - Check if the object is a solid rectangle/square (i.e., it completely fills its bounding box).
      - If an object is a solid rectangle/square, change the color of its interior pixels (pixels not on the border within the bounding box) to the background color (white, 0).
      - Leave non-solid objects and the background unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct objects in the input grid, where an object is a contiguous group of pixels with the same non-background color (not white).
    2.  For each identified object:
        a.  Determine the minimum bounding box that encloses the object.
        b.  Check if the object perfectly fills this bounding box (i.e., all pixels within the bounding box have the object's color). This identifies solid rectangles or squares.
        c.  If the object is a solid rectangle/square:
            i.  Identify the interior pixels of the object. These are the pixels within the bounding box that are not part of the outermost layer (top, bottom, left, right edges) of the object within that box.
            ii. Change the color of these interior pixels to the background color (white, 0).
        d.  If the object is not a solid rectangle/square, leave it unchanged.
    3.  Output the modified grid.
```python
import numpy as np
from collections import deque

"""
Identify contiguous non-background color objects.
For each object, determine its bounding box.
Check if the object is a solid rectangle/square (i.e., it completely fills its bounding box).
If an object is a solid rectangle/square, change the color of its interior pixels (pixels not on the border within the bounding box) to the background color (white, 0).
Leave non-solid objects and the background unchanged.
"""

def find_objects(grid, background_color=0):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color considered background.

    Returns:
        list: A list of dictionaries, each representing an object with 
              'color', 'pixels' (list of (r, c) tuples), and 
              'bounding_box' (min_r, max_r, min_c, max_c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If the pixel is not background and not visited yet, start search for a new object
            if grid[r, c] != background_color and not visited[r, c]:
                object_color = grid[r, c]
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    cr, cc = q.popleft()
                    current_object_pixels.append((cr, cc))

                    # Update bounding box
                    min_r = min(min_r, cr)
                    max_r = max(max_r, cr)
                    min_c = min(min_c, cc)
                    max_c = max(max_c, cc)

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = cr + dr, cc + dc
                        # Check bounds and if the neighbor is part of the same object
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == object_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found object
                objects.append({
                    'color': object_color,
                    'pixels': current_object_pixels,
                    'bounding_box': (min_r, max_r, min_c, max_c)
                })
    return objects

def is_solid_rectangle(grid, obj):
    """
    Checks if an object completely fills its bounding box.

    Args:
        grid (np.array): The input grid (used for context, could also just use obj['pixels']).
        obj (dict): The object dictionary containing 'color' and 'bounding_box'.

    Returns:
        bool: True if the object is a solid rectangle, False otherwise.
    """
    color = obj['color']
    min_r, max_r, min_c, max_c = obj['bounding_box']
    
    # Iterate through every cell within the bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # If any cell within the box does not match the object's color, it's not solid
            if grid[r, c] != color:
                return False
    # If all cells within the bounding box match the object's color, it's solid
    return True

def transform(input_grid):
    """
    Transforms the input grid by hollowing out solid rectangular/square objects.

    Args:
        input_grid (np.array): The input grid as a NumPy array.

    Returns:
        np.array: The transformed grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    background_color = 0

    # Find all objects in the grid
    objects = find_objects(input_grid, background_color)

    # Process each found object
    for obj in objects:
        # Check if the object is a solid rectangle
        if is_solid_rectangle(input_grid, obj):
            min_r, max_r, min_c, max_c = obj['bounding_box']
            
            # Hollow out the interior: iterate through pixels inside the border
            # Ensure there's an interior to hollow (i.e., width/height > 2)
            if max_r > min_r + 1 and max_c > min_c + 1:
                 for r in range(min_r + 1, max_r):
                    for c in range(min_c + 1, max_c):
                        output_grid[r, c] = background_color

    # Return the modified grid
    return output_grid
```
