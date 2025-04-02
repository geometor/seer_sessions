
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 0
4 4 4
```


## train_2

**input:**
```
0 0 3 3 0 0 0 0
0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0
0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
3 3
3 3
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 4 0 4 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0
0 0 3 0 0 3 0 0
0 0 0 3 3 0 0 0
```


**output:**
```
0 4 0
4 0 4
0 4 0
```

*   **Perception:** The input grids each contain two distinct objects composed of non-white pixels against a white background. The objects have different colors (yellow and green in the examples) and varying shapes. The output grid contains only one of these objects, cropped to its minimal bounding box. The core task is to identify the rule used to select which of the two objects is kept for the output. Comparing the examples, the selection criterion appears to be based on the vertical position of the objects: the object that appears higher up (i.e., has the minimum row index for any of its pixels) is the one selected.

*   **YAML Facts:**
    
```yaml
    task_structure:
      - description: Input grid contains a white background (0) and exactly two distinct non-white objects.
      - examples: 4 pairs provided.
      - goal: Select one of the two objects based on a rule and output it cropped to its bounding box.

    object_properties:
      - object: A contiguous area of pixels with the same non-white color.
      - attributes:
          - color: The pixel value (e.g., 3 for green, 4 for yellow).
          - pixels: A list of (row, col) coordinates belonging to the object.
          - bounding_box: The smallest rectangle containing all the object's pixels.
          - top_row_index: The minimum row index among all pixels of the object.

    relationships_and_actions:
      - count: There are always two non-white objects in the input.
      - comparison: The top_row_index of the two objects is compared.
      - selection: The object with the smaller top_row_index (the higher object) is selected.
      - transformation: The selected object is extracted.
      - output_generation: The output grid consists of the selected object, cropped to its bounding box. Any pixels outside the object within its bounding box remain white (0).

    assumptions:
      - There will always be exactly two non-white objects.
      - The two objects will not have the same minimum row index (no tie-breaking rule observed or needed based on examples).
    ```


*   **Natural Language Program:**
    1.  Identify all distinct contiguous objects of non-white pixels in the input grid.
    2.  Verify that exactly two such objects exist.
    3.  For each of the two objects, determine the row index of its topmost pixel (the minimum row index across all pixels belonging to that object).
    4.  Compare the topmost row indices of the two objects.
    5.  Select the object whose topmost row index is smaller (the object positioned higher in the grid).
    6.  Determine the bounding box of the selected object (the minimum and maximum row and column indices containing the object).
    7.  Create a new output grid whose dimensions match the height and width of the selected object's bounding box.
    8.  Populate the output grid by copying the pixels corresponding to the selected object from the input grid, adjusting their coordinates relative to the top-left corner of the bounding box. Fill any positions within the output grid that do not correspond to the selected object's pixels with the background color (white, 0).
```python
import numpy as np
from collections import deque

"""
Identify all distinct contiguous objects of non-white pixels in the input grid.
Verify that exactly two such objects exist.
For each object, determine its topmost row index.
Select the object with the smaller topmost row index (the higher object).
Crop the selected object to its bounding box and return it as the output grid.
Pixels within the bounding box but not part of the object remain white (0).
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-white pixels in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color', 'pixels' (set of (r, c) tuples),
              'bbox' (min_row, min_col, max_row, max_col), and 'top_row'.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                # Found the start of a new object
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))

                    # Update bounding box and top row
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'top_row': min_r
                })
    return objects

def crop_object(grid, obj):
    """
    Creates a new grid containing only the specified object,
    cropped to its bounding box.

    Args:
        grid (np.array): The original input grid (needed for pixel values).
        obj (dict): The object dictionary containing 'pixels' and 'bbox'.

    Returns:
        np.array: The cropped output grid.
    """
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    # Initialize output grid with background color (white)
    output_grid = np.zeros((height, width), dtype=int)

    # Copy object pixels to the output grid, adjusting coordinates
    for r, c in obj['pixels']:
        output_r = r - min_r
        output_c = c - min_c
        # Ensure coordinates are within the bounds of the new grid
        if 0 <= output_r < height and 0 <= output_c < width:
             output_grid[output_r, output_c] = grid[r, c] # Use original grid color

    return output_grid


def transform(input_grid):
    """
    Transforms the input grid according to the rule: find the highest
    of the two non-white objects and return it cropped to its bounding box.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)

    # Find all non-white objects in the grid
    objects = find_objects(grid_np)

    # Verify there are exactly two objects
    if len(objects) != 2:
        # This case shouldn't happen based on the examples, but good to handle
        # Returning an empty grid or raising an error could be options.
        # For now, let's return the input unchanged or an empty grid if undefined.
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning empty grid.")
        return [[]] # Or maybe return input_grid? Task description implies success case.

    # Find the object with the minimum top_row index (highest object)
    selected_object = min(objects, key=lambda obj: obj['top_row'])

    # Crop the selected object to its bounding box
    output_grid_np = crop_object(grid_np, selected_object)

    # Convert the output numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```
